const form = document.querySelector('#login-form');

const handleSubmit = async(e) => {
   e.preventDefault(); //리프레쉬 방지
   const formData = new FormData(form);
   const sha256Password = sha256(formData.get('password')); // sha256: 패스워드를 암호화해서 서버에 보낸다.
   formData.set('password', sha256Password);

   const res = await fetch('/login',{
      method: 'post',
      body: formData,
   });
   const data = await res.json();
   const accessToken = data.access_token;
   window.localStorage.setItem('token', accessToken);
   // window.sessionStorage.setItem('token', accessToken);
   alert('로그인 되었습니다!');
   
   window.location.pathname = "/";


   // console.log('액세스토큰!', data);
   // if(res.status === 200){
   //    alert('로그인에 성공했습니다!');
   //    window.location.pathname = "/";
   //    // console.log(data);
   //    console.log(res.status);
   // }else if (res.status === 401){
   //    alert('아이디 혹은 패스워드가 틀렸습니다.');
   // }

   const infoDiv = document.querySelector('#info');
   infoDiv.innerText = '로그인 되었습니다!'

   // window.location.pathname = "/";


   // const btn = document.createElement('button');
   // btn.innerText = '상품 가져오기!';
   // btn.addEventListener('click', async () => {
   //    const res = await fetch('/items',{
   //       headers: {
   //          'Authorization': `Bearer ${accessToken}`, // Bearer : prifix 같은 것.
   //       },
   //    });
   //    const data = await res.json();
   //    console.log(data);
   // });
   // infoDiv.appendChild(btn);
}

form.addEventListener('submit', handleSubmit);