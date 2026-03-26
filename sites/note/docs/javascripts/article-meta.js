document.addEventListener('DOMContentLoaded', function() {
  var article = document.querySelector('.md-content__inner');
  if (!article) return;
  // 跳过主页和时间线
  var h1 = article.querySelector('h1');
  if (!h1) return;
  var title = h1.textContent.trim();
  if (title === "Tardus Pura's Notes" || title === '更新时间线') return;

  var clone = article.cloneNode(true);
  var meta = clone.querySelector('.tp-article-meta');
  if (meta) meta.remove();
  var text = clone.textContent || '';

  // 字数
  var cn = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  var en = (text.match(/\b[a-zA-Z]+\b/g) || []).length;
  var words = cn + en;

  // 图片数
  var imgs = article.querySelectorAll('img').length;

  // 阅读时间
  var mins = Math.max(1, Math.ceil(cn / 300 + en / 200));

  var div = document.createElement('div');
  div.className = 'tp-article-meta';
  div.innerHTML =
    '<span>✏ 约 ' + words.toLocaleString() + ' 字</span>' +
    '<span>🖼 ' + imgs + ' 张图片</span>' +
    '<span>⏱ 预计阅读 ' + mins + ' 分钟</span>';

  h1.parentNode.insertBefore(div, h1.nextSibling);
});
