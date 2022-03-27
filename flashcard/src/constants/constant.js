export const REMOTE_URL = "http://localhost:5000/api/"
export function createDP(name) {
    if(name && typeof window !== undefined){
        let lname = name.split(" ")
        let initials = lname[0].charAt(0) + "" + (lname.length > 1 ? lname[lname.length - 1].charAt(0) : "")
        initials = String(initials).toUpperCase();
        var canvas = document.createElement('canvas');
        canvas.width = 200;
        canvas.height = 200;
        var ctx = canvas.getContext('2d');
        ctx.beginPath();
        ctx.rect(0, 0, 200, 200);
        ctx.closePath();
        ctx.fillStyle = '#144083';
        ctx.fill();
        ctx.fillStyle = "white";
        ctx.font = "bold 100px Arial";
        ctx.textAlign = 'center';
        ctx.fillText(initials, 105, 135);
        return canvas.toDataURL();
    }

    return ""
}

export function get_token(){
    let auth_token= localStorage.getItem('auth_token');
    if (!auth_token) {
        throw Error("Please login to continue")
    }
    return auth_token
}


function detectMimeType(b64) {
						
	var signatures = {
		'JVBERi0': "application/pdf",
		'R0lGODdh': "image/gif",
		'R0lGODlh': "image/gif",
		'iVBORw0KGgo': "image/png",
		"AAAA": "video/mp4",
		'/' : "image/jpg",
		'i' : "image/png",
		'R' : "image/gif",
		'U' : "image/webp",
		'J' : "application/pdf",
		'A' : "video/mp4",
    'UEsDBBQA' : "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;"
	};
	
	for (var s in signatures) {
		var i = b64.indexOf(s)
		if (i === 0 || i === 1) {
			return signatures[s];
		}
	}
}

export function fromBase64ToFile(s){
  var final = 'data:' + detectMimeType(s) + ";base64," + s;
  return final;
}
