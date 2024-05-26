<script>
    import { onMount } from "svelte";
    import Nav from "../components/Nav.svelte";
    import { getDatabase, ref, onValue } from "firebase/database";

   let hour = new Date().getHours();
   let min = new Date().getMinutes();

   // 랜더링
   $: items = [];

   const calcTime = (timestamp) => {
      const curTime = new Date().getTime() - 9*60*60*1000; //한국시간 -> 세계대표시간(URF)으로 계산해주기
      const time = new Date(curTime - timestamp);
      const hour = time.getHours();
      const minute = time.getMinutes();
      const second = time.getSeconds();

      if(hour > 0) return `${hour}시간 전`
      else if(minute > 0) return `${minute}분 전`
      else if(second > 0) return `${second}초 전`
      else return `방금 전`
   };

   const db = getDatabase();
   const itemsRef = ref(db, "items/");

   onMount(() => { //onMount : 화면이 보여질때마다 실행. (다른 js는 한번만 실행하기 때문에)
      onValue(itemsRef, (snapshot) => {
         const data = snapshot.val();
         items = Object.values(data).reverse(); //값이 바뀔때마다 업데이트
      });
   });
   
</script>

<header>
   <div class="info-bar">
      <div class="info-bar__time">{hour}:{min}</div>
      <div class="info-bar__icons">
         <img src="assets/chart-bar.svg" alt="chart-bar" />
         <img src="assets/wifi.svg" alt="wifi" />
         <img src="assets/battery.svg" alt="battery" />
      </div>
   </div>
   <div class="menu-bar">
      <div class="menu-bar__location">
         <div>역삼1동</div>
         <div class="menu-bar__location-icon">
            <img src="assets/arrow-down.svg" alt="arrow-down" />
         </div>
      </div>
      <div class="menu-bar__icons">
         <img src="assets/search.svg" alt="search" />
         <img src="assets/menu.svg" alt="menu" />
         <img src="assets/alert.svg" alt="alert" />
      </div>
   </div>
</header>

<main>
   {#each items as item}
   <div class="item-list">
      <div class="item-list__img">
         <img alt={item.title} src={item.imgUrl} />
      </div>
      <div class="item-list__info">
         <div class="item-list__info-title">{item.title}</div>
         <div class="item-list__info-meta">{item.price} {calcTime(item.insertAt)}</div>
         <div class="item-list__info-price">{item.place}</div>
         <div class="item-list__info-description">{item.description}</div>
      </div>
   </div>
   {/each}
   <a class="write-btn" href="#/write">+ 글쓰기</a>
</main>

<Nav location='home' />

<div class="media-info-msg">화면을 줄여주세요!</div>
