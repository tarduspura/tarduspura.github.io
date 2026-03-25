// 主页统计数据（由 update_stats.py 在构建时自动更新）
document.addEventListener('DOMContentLoaded', function() {
  var noteEl = document.getElementById('tp-note-count');
  var wordEl = document.getElementById('tp-word-count');
  if (noteEl) noteEl.textContent = '20';
  if (wordEl) wordEl.textContent = '22,952';
});
