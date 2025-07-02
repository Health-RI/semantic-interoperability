document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('tableSearchInput');
  if (!searchInput) return;

  searchInput.addEventListener('input', function() {
    const filter = searchInput.value.toLowerCase();
    document.querySelectorAll('table tbody tr').forEach(function(row) {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(filter) ? '' : 'none';
    });
  });
});
