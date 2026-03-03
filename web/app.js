const вкладки = document.querySelectorAll('.tab');
const панели = document.querySelectorAll('.panel');

for (const кнопка of вкладки) {
  кнопка.addEventListener('click', () => {
    for (const t of вкладки) t.classList.remove('active');
    кнопка.classList.add('active');

    const id = кнопка.dataset.tab;
    for (const панель of панели) {
      панель.classList.toggle('active', панель.id === id);
    }
  });
}

const singleQuality = document.getElementById('singleQuality');
const singleQualityValue = document.getElementById('singleQualityValue');
singleQuality.addEventListener('input', () => (singleQualityValue.textContent = singleQuality.value));

const batchQuality = document.getElementById('batchQuality');
const batchQualityValue = document.getElementById('batchQualityValue');
batchQuality.addEventListener('input', () => (batchQualityValue.textContent = batchQuality.value));

document.getElementById('singleRun').addEventListener('click', async () => {
  const путь = document.getElementById('singlePath').value;
  const формат = document.getElementById('singleFormat').value;
  const качество = Number(document.getElementById('singleQuality').value);
  const статус = document.getElementById('singleStatus');

  const ответ = await eel.конвертировать_один(путь, формат, качество)();
  статус.textContent = ответ.message;
  статус.classList.toggle('error', !ответ.ok);
});

document.getElementById('batchRun').addEventListener('click', async () => {
  const путь = document.getElementById('batchPath').value;
  const формат = document.getElementById('batchFormat').value;
  const качество = Number(document.getElementById('batchQuality').value);
  const статус = document.getElementById('batchStatus');

  const ответ = await eel.конвертировать_пачку(путь, формат, качество)();
  статус.textContent = ответ.message;
  статус.classList.toggle('error', !ответ.ok);
});
