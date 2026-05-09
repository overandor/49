function fmt(obj) { return JSON.stringify(obj, null, 2); }

function setReport(data) {
  const score = data.score || {};
  document.getElementById('state').textContent = score.state || 'Unknown';
  document.getElementById('score').textContent = (score.final_score ?? 0).toFixed ? score.final_score.toFixed(2) : score.final_score || '0.00';
  document.getElementById('verification').textContent = fmt(data.verification || {});
  document.getElementById('scoreJson').textContent = fmt(score);
  document.getElementById('report').textContent = data.report_markdown || 'No report returned.';
}

async function postForm(url, body) {
  const resp = await fetch(url, { method: 'POST', body });
  if (!resp.ok) throw new Error(await resp.text());
  return await resp.json();
}

document.getElementById('demoBtn').addEventListener('click', async () => {
  document.getElementById('report').textContent = 'Generating demo report...';
  const data = await postForm('/api/demo-report', new FormData());
  setReport(data);
});

document.getElementById('mockBtn').addEventListener('click', async () => {
  const fd = new FormData();
  fd.append('project_name', document.getElementById('projectName').value);
  fd.append('readme', document.getElementById('readme').value);
  document.getElementById('report').textContent = 'Analyzing mock project...';
  const data = await postForm('/api/mock-upload-report', fd);
  setReport(data);
});

document.getElementById('llmBtn').addEventListener('click', async () => {
  const fd = new FormData();
  fd.append('text', document.getElementById('archiveText').value);
  document.getElementById('llmOutput').textContent = 'Calling public no-key LLM or fallback...';
  const data = await postForm('/api/analyze-text', fd);
  document.getElementById('llmOutput').textContent = fmt(data);
});
