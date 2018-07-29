function check() {
    if(document.frm1.name.value == ""){
        alert("이름을 입력해주세요!");
        document.frm1.name.focus();
    } else if (document.frm1.subject.value == ""){
        alert("제목을 입력해주세요!");
        document.frm1.subject.focus();
    } else if (document.frm1.content.value == ""){
        alert("내용을 입력해주세요!");
        document.frm1.content.focus();
    } else {
        document.frm1.submit();
    }
}