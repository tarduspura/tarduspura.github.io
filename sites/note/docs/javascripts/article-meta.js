document.addEventListener('DOMContentLoaded', function() {
  // 跳过首页和时间线页面（通过URL判断）
  var path = window.location.pathname;
  if (path.endsWith('/note/') || path.endsWith('/note') ||
      path.endsWith('/changelog/') || path.endsWith('/changelog')) return;

  var article = document.querySelector('.md-content__inner');
  if (!article) return;
  var h1 = article.querySelector('h1');
  if (!h1) return;

  var clone = article.cloneNode(true);
  var meta = clone.querySelector('.tp-article-meta');
  if (meta) meta.remove();
  var text = clone.textContent || '';

  var cn = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  var en = (text.match(/\b[a-zA-Z]+\b/g) || []).length;
  var words = cn + en;
  var imgs = article.querySelectorAll('img').length;
  var mins = Math.max(1, Math.ceil(cn / 300 + en / 200));

  var div = document.createElement('div');
  div.className = 'tp-article-meta';
  div.innerHTML =
    '<span>✏ 约 ' + words.toLocaleString() + ' 字</span>' +
    '<span>🖼 ' + imgs + ' 张图片</span>' +
    '<span>⏱ 预计阅读 ' + mins + ' 分钟</span>';

  h1.parentNode.insertBefore(div, h1.nextSibling);
});
