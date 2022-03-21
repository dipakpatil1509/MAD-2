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

var crypto = require('crypto');

export function cipher_encryption(text, secrete) {
    return encrypt(Buffer.from(String(text),'utf-8'), Buffer.from(String(secrete), 'utf-8'));
}

export function cipher_decryption(enc, secrete) {
    return decrypt(Buffer.from(String(enc),'hex'), Buffer.from(String(secrete), 'utf-8'));
}


const ALGORITHM = 'aes-256-cbc'

const encrypt = (dataBuffer, keyBuffer) => {
  // iv stands for "initialization vector"
  const iv = crypto.randomBytes(12)
  const cipher = crypto.createCipheriv(ALGORITHM, keyBuffer, iv)
  const encryptedBuffer = Buffer.concat([cipher.update(dataBuffer), cipher.final()])
  const authTag = cipher.getAuthTag()
  let bufferLength = Buffer.alloc(1)
  bufferLength.writeUInt8(iv.length, 0)
  return Buffer.concat([bufferLength, iv, authTag, encryptedBuffer]).toString('hex')
}

const decrypt = (dataBuffer, keyBuffer) => {
  console.log(dataBuffer + "");
  dataBuffer = Buffer.from(dataBuffer,'base64')
  console.log(dataBuffer + "");
  const ivSize = 16
  const iv = dataBuffer.slice(0, ivSize)
  console.log(iv + "");
//   const authTag = dataBuffer.slice(ivSize + 1, ivSize + 17)
  const decipher = crypto.createDecipheriv(ALGORITHM, keyBuffer, iv);
  console.log(decipher);
  console.log(decipher.update(dataBuffer.slice(ivSize))) + "";
  let decrypt = String.fromCharCode.apply(String, decipher.update(dataBuffer.slice(ivSize)))
  console.log(decrypt);
//   decipher.setAuthTag(authTag)
  return String(decrypt)
}