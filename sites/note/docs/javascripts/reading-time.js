// 自动计算并显示文章字数和阅读时间
document.addEventListener('DOMContentLoaded', function() {
  // 获取文章内容
  const article = document.querySelector('.md-content__inner');
  if (!article) return;
  
  // 排除标题和元信息区域
  const content = article.cloneNode(true);
  const title = content.querySelector('h1');
  const existingMeta = content.querySelector('.article-meta');
  if (title) title.remove();
  if (existingMeta) existingMeta.remove();
  
  // 获取纯文本
  const text = content.textContent || content.innerText;
  
  // 统计中文字符
  const chineseChars = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  
  // 统计英文单词
  const englishWords = (text.match(/\b[a-zA-Z]+\b/g) || []).length;
  
  // 总字数
  const totalWords = chineseChars + englishWords;
  
  // 计算阅读时间（中文300字/分钟，英文200词/分钟）
  const readingTime = Math.ceil((chineseChars / 300) + (englishWords / 200));
  
  // 创建元信息元素
  const metaDiv = document.createElement('div');
  metaDiv.className = 'article-meta';
  metaDiv.innerHTML = `
    <span>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
        <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
      </svg>
      ${totalWords.toLocaleString()} 字
    </span>
    <span>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
        <path d="M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z" />
      </svg>
      约 ${readingTime} 分钟
    </span>
  `;
  
  // 插入到标题后面
  const h1 = article.querySelector('h1');
  if (h1 && h1.nextSibling) {
    h1.parentNode.insertBefore(metaDiv, h1.nextSibling);
  } else if (h1) {
    h1.parentNode.appendChild(metaDiv);
  }
});
