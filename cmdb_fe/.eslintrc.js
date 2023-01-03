module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: ['plugin:vue/vue3-essential', 'eslint:recommended', 'plugin:prettier/recommended'],
  parserOptions: {
    parser: '@babel/eslint-parser'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'vue/multi-word-component-names': 'off', // 关闭组件命名规则
    quotes: [1, 'single'], // 引号类型 `` "" ''
    'no-extra-semi': 2, // 禁止多余的冒号
    'space-before-function-paren': [0, 'always'] // 函数定义时括号前面要不要有空格
  }
}
