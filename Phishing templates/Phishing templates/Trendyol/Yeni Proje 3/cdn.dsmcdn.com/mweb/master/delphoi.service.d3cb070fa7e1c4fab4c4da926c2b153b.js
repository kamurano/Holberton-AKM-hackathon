var _delphoiUrl,_isAEventFlowEnabled,_caq=_caq||{},_gcol=_gcol||{unUsedParameters:["rootUrl"],rootUrl:_caq.rootUrl,channel:_caq.channel};try{_delphoiUrl=document.getElementById("delphoi-script").getAttribute("data-append-url"),_isAEventFlowEnabled="true"===document.getElementById("delphoi-script").getAttribute("data-a-event-flow")}catch(e){_delphoiUrl="",_isAEventFlowEnabled=!1,console.warn(e)}_gcol.ReadCookie=function(e){for(var n=e+"=",o=document.cookie.split(";"),r=0;r<o.length;r++){for(var t=o[r];" "===t.charAt(0);)t=t.substring(1,t.length);if(0===t.indexOf(n))return t.substring(n.length,t.length)}return null},_gcol.GetPid=function(){var e=_gcol.ReadCookie("pid");return null===e&&(e=_gcol.ReadCookie("pid_alt")),{pid:e}},_gcol.GetSid=function(){return{sid:_gcol.ReadCookie("sid")}},_gcol.HasSidAndPid=function(){return!!_gcol.GetPid().pid&&!!_gcol.GetSid().sid},_gcol.AppendPixel=function(e){var n=_delphoiUrl+"/__gc.gif?_="+Math.random().toString().slice(12)+"&p="+this.RemoveAndEncodeParameters(e),o=document.createElement("img");o.src=n,o.id=Math.random()+"_pixel",o.style.display="none",document.body.insertBefore(o,document.body.firstChild),document.body.removeChild(o)},_gcol.HasWebBeaconSupport=function(){return!!navigator&&!!navigator.sendBeacon},_gcol.SendWebBeacon=function(e){var n=_delphoiUrl+"/e",o=_gcol.GetBeaconData(e);return navigator.sendBeacon(n,new Blob([JSON.stringify(o)],{type:"text/plain; charset=UTF-8"}))||_gcol.AppendPixel(e)},_gcol.SendAWebBeacon=function(e){var n=_delphoiUrl+"/ea",o=_gcol.GetBeaconData(e);return o.pid=void 0,o.sid=void 0,navigator.sendBeacon(n,new Blob([JSON.stringify(o)],{type:"text/plain; charset=UTF-8"}))},_gcol.Send=function(e,n){var o=n&&n.forceGetPidAndSid,r=n&&n.getPidSid,t=_gcol.HasSidAndPid();return _gcol.HasWebBeaconSupport()&&t?_gcol.SendWebBeacon(e):r?_gcol.AppendPixel(e,n):_isAEventFlowEnabled&&!t?_gcol.SendAWebBeacon(e):o?_gcol.SendWebBeacon(e):_gcol.AppendPixel(e,n)},_gcol.Fire=function(e,n,o){if("string"!=typeof e)throw new Error("missing event name parameter");if(n){n.channel=_gcol.channel,n.event=e;try{window.demeterInstance&&window.demeterInstance.adapt("delphoi",n,o).send()}catch(e){console.error(e)}return _gcol.Send(n,o)}},_gcol.RemoveAndEncodeParameters=function(e,n){var o=this,r=o.getBrowserInformation();e.ref=o.getReferrer(),n&&n.includeAdditionalData&&(e.operatingSystem=r.os,e.bv=r.bv,e.bn=r.bn,e.screenResolution=o.getResolution());for(var t=e,i=o.unUsedParameters.length,a=0;a<i;a++)delete t[o.unUsedParameters[a]];for(var a in t)null!==t[a]&&void 0!==t[a]||delete t[a];return encodeURIComponent(_gcol.psv(t))},_gcol.GetBeaconData=function(e,n){var o=this,r=o.getBrowserInformation();e.ref=o.getReferrer(),e.pid=_gcol.GetPid().pid||"null",e.sid=_gcol.GetSid().sid||"null",e.sr="beacon",n&&n.includeAdditionalData&&(e.operatingSystem=r.os,e.bv=r.bv,e.bn=r.bn,e.screenResolution=o.getResolution());for(var t=e,i=o.unUsedParameters.length,a=0;a<i;a++)delete t[o.unUsedParameters[a]];return t},_gcol.escape=function(e){if("string"==typeof e)return e.replace(/\|/g,"\\|")},_gcol.psv=function(e){var n=[];for(var o in e)n.push(o),n.push(_gcol.escape(e[o]));return n.join("||")},_gcol.getResolution=function(){return window.screen.availWidth+"x"+window.screen.availHeight},_gcol.getReferrer=function(){var e=document.referrer,n=document.location.host;return e.indexOf(n)<0?document.referrer:""},_gcol.getBrowserInformation=function(){navigator.appVersion;var e,n,o,r=navigator.userAgent,t=navigator.appName,i=""+parseFloat(navigator.appVersion),a=parseInt(navigator.appVersion,10);-1!=(n=r.indexOf("Opera"))?(t="Opera",i=r.substring(n+6),-1!=(n=r.indexOf("Version"))&&(i=r.substring(n+8))):-1!=(n=r.indexOf("MSIE"))?(t="Microsoft Internet Explorer",i=r.substring(n+5)):-1!=(n=r.indexOf("Chrome"))?(t="Chrome",i=r.substring(n+7)):-1!=(n=r.indexOf("Safari"))?(t="Safari",i=r.substring(n+7),-1!=(n=r.indexOf("Version"))&&(i=r.substring(n+8))):-1!=(n=r.indexOf("Firefox"))?(t="Firefox",i=r.substring(n+8)):(e=r.lastIndexOf(" ")+1)<(n=r.lastIndexOf("/"))&&(t=r.substring(e,n),i=r.substring(n+1),t.toLowerCase()==t.toUpperCase()&&(t=navigator.appName)),-1!=(o=i.indexOf(";"))&&(i=i.substring(0,o)),-1!=(o=i.indexOf(" "))&&(i=i.substring(0,o)),a=parseInt(""+i,10),isNaN(a)&&(i=""+parseFloat(navigator.appVersion),a=parseInt(navigator.appVersion,10));var d="Unknown OS";return-1!=navigator.appVersion.indexOf("Win")&&(d="Windows"),-1!=navigator.appVersion.indexOf("Mac")&&(d="MacOS"),-1!=navigator.appVersion.indexOf("X11")&&(d="UNIX"),-1!=navigator.appVersion.indexOf("Linux")&&(d="Linux"),{os:d,bv:i,bn:t}},"undefined"!=typeof module&&module.exports&&(exports._gcol=_gcol);