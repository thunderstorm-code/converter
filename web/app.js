const tabs = document.querySelectorAll('.tab');
const panels = document.querySelectorAll('.panel');

for (const button of tabs) {
  button.addEventListener('click', () => {
    for (const tab of tabs) tab.classList.remove('active');
    button.classList.add('active');

    const id = button.dataset.tab;
    for (const panel of panels) {
      panel.classList.toggle('active', panel.id === id);
    }
  });
}

async function runTelethonToTdata() {
  const status = document.getElementById('statusToTdata');
  status.classList.remove('error');
  status.textContent = 'Working...';

  const response = await eel.convert_telethon({
    sessionPath: document.getElementById('sessionPath').value,
    outputDir: document.getElementById('outputDir').value,
  })();

  status.textContent = response.message;
  status.classList.toggle('error', !response.ok);
}

async function runTdataToTelethon() {
  const status = document.getElementById('statusToTelethon');
  status.classList.remove('error');
  status.textContent = 'Working...';

  const response = await eel.convert_tdata({
    tdataDir: document.getElementById('tdataDir').value,
    outputSessionPath: document.getElementById('outputSessionPath').value,
  })();

  status.textContent = response.message;
  status.classList.toggle('error', !response.ok);
}

document.getElementById('runToTdata').addEventListener('click', runTelethonToTdata);
document.getElementById('runToTelethon').addEventListener('click', runTdataToTelethon);
