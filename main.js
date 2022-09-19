var kodevist=false;


function viskode() {
    kodevist=!kodevist;
    var knap=document.getElementById("viskodeid");
    if(!kodevist) {
        knap.innerHTML="<b>Vis kode</b>";
    }else {
        knap.innerHTML="<b>Skjul kode</b>";
    }
}
setInterval(checkhover, 16);
function checkhover() {
    
    var divlist=[
        "eksempelh", "eksempeltekst", "eksempelknap", "eksempelfelt"
    ]
    if(kodevist) {
        var elements=document.querySelectorAll(":hover");
        var eksn=-1;
        for(var i=0;i<elements.length;i++) {
            if(elements[i].id=="normaltekst") {
                eksn=1;
            }else if(elements[i].tagName=="H1" || elements[i].tagName=="H2") {
                eksn=0;
            }else if(elements[i].tagName=="BUTTON") {
                eksn=2;
            }else if(elements[i].id=="centerdiv") {
                eksn=3;
            }
        }
        for(var j=0;j<divlist.length;j++) {
            if(j==eksn) {
                document.getElementById(divlist[j]).style.display="block";
            }else{
                document.getElementById(divlist[j]).style.display="none";
            }
        }
    }else {
        for(var j=0;j<divlist.length;j++) {
            document.getElementById(divlist[j]).style.display="none";
        }
    }
    
}