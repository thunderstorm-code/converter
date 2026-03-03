const tabs = document.querySelectorAll('.tab');
const panels = document.querySelectorAll('.panel');
const convertButton = document.getElementById('convertButton');
const progressWrap = document.getElementById('progressWrap');
const progressBar = document.getElementById('progressBar');

const formState = {
  mode: 'toTdata',
  toTdata: { sessionPath: '', outputDir: '' },
  toTelethon: { tdataDir: '', outputDir: '' },
};

function setStatus(text, isError = false) {
  const id = formState.mode === 'toTdata' ? 'statusToTdata' : 'statusToTelethon';
  const el = document.getElementById(id);
  el.textContent = text;
  el.classList.toggle('error', isError);
}

function updateConvertState() {
  const ready = formState.mode === 'toTdata'
    ? Boolean(formState.toTdata.sessionPath && formState.toTdata.outputDir)
    : Boolean(formState.toTelethon.tdataDir && formState.toTelethon.outputDir);

  convertButton.disabled = !ready;
  convertButton.classList.toggle('ready', ready);
}

function switchTab(mode) {
  formState.mode = mode;
  for (const tab of tabs) tab.classList.toggle('active', tab.dataset.tab === mode);
  for (const panel of panels) panel.classList.toggle('active', panel.id === mode);
  updateConvertState();
}

async function chooseSession() {
  const picked = await eel.pick_session_file()();
  if (!picked.path) return;
  formState.toTdata.sessionPath = picked.path;
  document.getElementById('sessionName').value = picked.name;
  updateConvertState();
}

async function chooseTdata() {
  const picked = await eel.pick_tdata_folder()();
  if (!picked.path) return;
  formState.toTelethon.tdataDir = picked.path;
  document.getElementById('tdataName').value = picked.name;
  updateConvertState();
}

async function chooseSaveToTdata() {
  const picked = await eel.pick_output_folder()();
  if (!picked.path) return;
  formState.toTdata.outputDir = picked.path;
  document.getElementById('saveNameToTdata').value = picked.name;
  updateConvertState();
}

async function chooseSaveToTelethon() {
  const picked = await eel.pick_output_folder()();
  if (!picked.path) return;
  formState.toTelethon.outputDir = picked.path;
  document.getElementById('saveNameToTelethon').value = picked.name;
  updateConvertState();
}

function startProgress() {
  progressWrap.classList.add('active');
  progressBar.style.width = '0%';
  let value = 0;
  return setInterval(() => {
    if (value < 92) {
      value += 4;
      progressBar.style.width = `${value}%`;
    }
  }, 120);
}

function finishProgress(timer) {
  clearInterval(timer);
  progressBar.style.width = '100%';
  setTimeout(() => {
    progressWrap.classList.remove('active');
    progressBar.style.width = '0%';
  }, 350);
}

async function runConversion() {
  if (convertButton.disabled) return;

  setStatus('Conversion started...');
  const timer = startProgress();

  let response;
  if (formState.mode === 'toTdata') {
    response = await eel.convert_telethon(formState.toTdata)();
  } else {
    response = await eel.convert_tdata(formState.toTelethon)();
  }

  finishProgress(timer);
  setStatus(response.message, !response.ok);
}

for (const button of tabs) {
  button.addEventListener('click', () => switchTab(button.dataset.tab));
}

document.getElementById('pickSession').addEventListener('click', chooseSession);
document.getElementById('pickTdata').addEventListener('click', chooseTdata);
document.getElementById('pickSaveToTdata').addEventListener('click', chooseSaveToTdata);
document.getElementById('pickSaveToTelethon').addEventListener('click', chooseSaveToTelethon);
document.getElementById('convertButton').addEventListener('click', runConversion);

updateConvertState();
