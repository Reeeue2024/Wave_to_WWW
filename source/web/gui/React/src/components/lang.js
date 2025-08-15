// React/src/components/lang.js

export function getLang() {
  let lang = localStorage.getItem('lang');
  if (!lang) {
    lang = 'en'; // 기본 언어
    localStorage.setItem('lang', lang);
  }
  return lang;
}