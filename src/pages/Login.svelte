<script>
   import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
   import { user$ } from "../store";

   const provider = new GoogleAuthProvider();
   const auth = getAuth();

   const loginWithGoogle = async () => {
      try {
         const result = await signInWithPopup(auth, provider)
         const credential = GoogleAuthProvider.credentialFromResult(result);
         const token = credential.accessToken;
         const user = result.user;
         user$.set(user);
         localStorage.setItem('token', token);
      } catch(error){
         console.error(error);
      }
   }

</script>

<div>
   <div>로그인하기</div>
   <button class="login-btn" on:click={loginWithGoogle}>
      <img
      class="google-img"
      src="https://png.pngtree.com/png-vector/20230817/ourmid/pngtree-google-internet-icon-vector-png-image_9183287.png"
      alt="" />
      <div>Google로 로그인하기</div>
      <div />
   </button>
</div>

<style>
   .login-btn {width: 200px;height:50px;border: 1px solid gray;display: flex;justify-content: space-between;align-items: center;border-radius: 3px;}
   .google-img {width: 20px;}
</style>