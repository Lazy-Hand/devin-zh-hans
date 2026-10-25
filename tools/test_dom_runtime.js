/* 验证 DOM 层只翻译输入框 placeholder，不修改输入内容。 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

function element(tagName, attrs = {}) {
  return {
    nodeType: 1,
    tagName,
    attrs: { ...attrs },
    parentElement: null,
    isContentEditable: false,
    getAttribute(name) { return this.attrs[name] ?? null; },
    setAttribute(name, value) { this.attrs[name] = value; },
    matches() { return false; },
    querySelectorAll() { return []; },
  };
}

const input = element('INPUT', { placeholder: 'Search all models', value: 'User text stays unchanged' });
const editable = element('INPUT', { placeholder: 'Search all models' });
editable.isContentEditable = true;
const body = element('BODY');
body.querySelectorAll = (selector) => selector.includes('input[placeholder]') ? [input, editable] : [];
input.parentElement = body;
editable.parentElement = body;
const documentElement = element('HTML');
body.parentElement = documentElement;

let observerOptions = null;
const document = {
  body,
  documentElement,
  createTreeWalker() { return { nextNode() { return null; } }; },
  addEventListener() {},
};
const window = {
  setTimeout() { return 1; },
  setInterval() { return 1; },
  clearInterval() {},
  requestAnimationFrame(fn) { fn(); return 1; },
};
const context = {
  window,
  document,
  console: { log() {} },
  NodeFilter: { SHOW_TEXT: 4, FILTER_ACCEPT: 1, FILTER_REJECT: 2 },
  MutationObserver: class {
    constructor(callback) { this.callback = callback; }
    observe(_target, options) { observerOptions = options; }
  },
  WeakSet,
};
window.MutationObserver = context.MutationObserver;
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../dist/devin-zh-dom.js'), 'utf8'), context);

const results = [
  [input.attrs.placeholder === '搜索所有模型', '普通输入框 placeholder 已翻译'],
  [input.attrs.value === 'User text stays unchanged', '输入内容未被修改'],
  [editable.attrs.placeholder === 'Search all models', 'contenteditable 区域保持跳过'],
  [observerOptions && observerOptions.attributes === true
    && observerOptions.attributeFilter.includes('placeholder'), 'placeholder 属性变化已纳入观察'],
];
let failed = 0;
for (const [ok, label] of results) {
  console.log((ok ? '✓ ' : '✗ ') + label);
  if (!ok) failed++;
}
console.log((results.length - failed) + '/' + results.length + ' 通过');
process.exit(failed ? 1 : 0);
