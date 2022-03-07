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