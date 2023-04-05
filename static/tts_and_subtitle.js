const synth = window.speechSynthesis;

const WS_SERVER_URL = "http://localhost:7777/tts";
const SOCKETIO_NAMESPACE = '/tts'

const subtitleTxt = document.getElementById("subtitle_text");
let style = window.getComputedStyle(subtitleTxt, null).getPropertyValue('font-size');
const DEFAULT_FONT_SIZE = parseFloat(style);

const VOICE_NAME = "Microsoft Xiaoyi Online (Natural) - Chinese (Mainland)"
let voices = [];
let textList = [];
let socket;
let voice;

function setVoice() {
  const voices = synth.getVoices()
  for (var i in voices) {
    console.log(voices[i].name)
    if (voices[i].name === VOICE_NAME) {
      console.log('Voice set: ' + voices[i].name);
      voice = voices[i];
      return ;
    }
  }
  voice = voices[0];
}

setVoice()

if (speechSynthesis.onvoiceschanged !== undefined) {
  speechSynthesis.onvoiceschanged = setVoice;
}

function updateSubtitle(text) {
  const view_width = document.body.clientWidth;   // 计算 font-size 的值
  const font_size  = Math.min(DEFAULT_FONT_SIZE * 2, Math.max(DEFAULT_FONT_SIZE, Math.floor(view_width/(text.length))))  // 设置当前的 html 的 font-size 属性的值 
  subtitleTxt.style.fontSize = font_size + 'px';
  subtitleTxt.innerHTML = text
}

function speakNext(rate=1., pitch=1.) {
  if (synth.speaking) {
    console.error("speechSynthesis.speaking");
    return ;
  }

  if (textList.length == 0) {
    socket.emit('tts_finished', namespace=SOCKETIO_NAMESPACE)
    return ;
  }

  const text = textList.shift()
  const utterThis = new SpeechSynthesisUtterance(text);

  utterThis.onend = function (event) {
    console.log("SpeechSynthesisUtterance.onend");
    updateSubtitle(text)
    speakNext()
  };

  utterThis.onerror = function (event) {
    console.error("SpeechSynthesisUtterance.onerror");
    speakNext()
  };

  utterThis.onboundary = (event) => {
    console.log(
      `${text.slice(event.charIndex, event.charIndex+event.charLength)}`
    );
    updateSubtitle(text.slice(0, event.charIndex+event.charLength))
  };
  
  utterThis.voice = voice;
  utterThis.pitch = pitch;
  utterThis.rate = rate;
  synth.speak(utterThis);
}

socket = io.connect(WS_SERVER_URL);

socket.on('connect', function (data) {
  console.log("start connection");
});

socket.on('disconnect', function(data){
  console.log("connection closed");
});
    
socket.on('tts', function (data) {
  const text = data.text.trim();
  if (text !== "") {
    textList.push(text);
    console.log(textList);
    speakNext();
  }
});
