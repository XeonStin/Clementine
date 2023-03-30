const synth = window.speechSynthesis;

const WS_SERVER_URL = "http://localhost:7777/tts";
const SOCKETIO_NAMESPACE = '/tts'

const subtitleTxt = document.getElementById("subtitle_text");
let style = window.getComputedStyle(subtitleTxt, null).getPropertyValue('font-size');
const DEFAULT_FONT_SIZE = parseFloat(style);

let voices = [];
let textList = [];
let isSpeaking = false;
let socket;

function populateVoiceList() {
  voices = synth.getVoices().sort(function (a, b) {
    const aname = a.name.toUpperCase();
    const bname = b.name.toUpperCase();

    if (aname < bname) {
      return -1;
    } else if (aname == bname) {
      return 0;
    } else {
      return +1;
    }
  });

  for (let i = 0; i < voices.length; i++) {
    const option = document.createElement("option");
    option.textContent = `${voices[i].name} (${voices[i].lang})`;

    if (voices[i].default) {
      option.textContent += " -- DEFAULT";
    }

    option.setAttribute("data-lang", voices[i].lang);
    option.setAttribute("data-name", voices[i].name);
  }
}

populateVoiceList();

if (speechSynthesis.onvoiceschanged !== undefined) {
  speechSynthesis.onvoiceschanged = populateVoiceList;
}
/*
function speak(text="", rate=1., pitch=1.) {
  if (synth.speaking) {
    console.error("speechSynthesis.speaking");
    return;
  }

  if (text !== "") {
    const utterThis = new SpeechSynthesisUtterance(text);

    utterThis.onend = function (event) {
      console.log("SpeechSynthesisUtterance.onend");
      socket.emit('tts_finished', namespace=SOCKETIO_NAMESPACE)
    };

    utterThis.onerror = function (event) {
      console.error("SpeechSynthesisUtterance.onerror");
      socket.emit('tts_finished', namespace=SOCKETIO_NAMESPACE)
    };

    utterThis.onboundary = (event) => {
      console.log(
        `${text.slice(event.charIndex, event.charIndex+event.charLength)}`
      );
      const view_width = document.body.clientWidth;   // 计算 font-size 的值
      const font_size  = Math.min(DEFAULT_FONT_SIZE * 2, Math.max(DEFAULT_FONT_SIZE, Math.floor(view_width/(event.charIndex+event.charLength))))  // 设置当前的 html 的 font-size 属性的值 
      subtitleTxt.style.fontSize = font_size + 'px';
      subtitleTxt.innerHTML = text.slice(0, event.charIndex+event.charLength)
    };

    const selectedOption = "Microsoft Xiaoyi Online (Natural) - Chinese (Mainland)"

    for (let i = 0; i < voices.length; i++) {
      if (voices[i].name === selectedOption) {
        utterThis.voice = voices[i];
        break;
      }
    }
    utterThis.pitch = pitch;
    utterThis.rate = rate;
    synth.speak(utterThis);
  }
}
*/
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

  if (text !== "") {
    const utterThis = new SpeechSynthesisUtterance(text);

    utterThis.onend = function (event) {
      console.log("SpeechSynthesisUtterance.onend");
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
      const view_width = document.body.clientWidth;   // 计算 font-size 的值
      const font_size  = Math.min(DEFAULT_FONT_SIZE * 2, Math.max(DEFAULT_FONT_SIZE, Math.floor(view_width/(event.charIndex+event.charLength))))  // 设置当前的 html 的 font-size 属性的值 
      subtitleTxt.style.fontSize = font_size + 'px';
      subtitleTxt.innerHTML = text.slice(0, event.charIndex+event.charLength)
    };

    const selectedOption = "Microsoft Xiaoyi Online (Natural) - Chinese (Mainland)"

    for (let i = 0; i < voices.length; i++) {
      if (voices[i].name === selectedOption) {
        utterThis.voice = voices[i];
        break;
      }
    }
    utterThis.pitch = pitch;
    utterThis.rate = rate;
    synth.speak(utterThis);
  }
}

$(document).ready(function () {
  socket = io.connect(WS_SERVER_URL);
  
  socket.on('connect', function (data) {
    console.log("start connection");
  });
  
  socket.on('disconnect', function(data){
    console.log("connection closed");
  });
      
  socket.on('tts', function (data) {
    const text = data.text;
    textList.push(text);
    console.log(textList);
    speakNext();
  });
});