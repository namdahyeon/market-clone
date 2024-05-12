const form = document.getElementById('write-form');

const handleSubmitForm = async (e) => {
   e.preventDefault();
   const body = new FormData(form);
   body.append('insertAt',new Date().getTime());

   try{
      const res = await fetch('/items',{
         method:'POST',
         body,
      });
      const data = await res.json();
      if (data === '200') window.location.pathname = "/";
   }catch(e){
      // 에러에 관한 내용 출력
      console.error(e);
   }
};

form.addEventListener('submit',handleSubmitForm);