{/* <div class="item-list">
   <div class="item-list__img">
      <img src="assets/img.svg" alt="" />
   </div>
   <div class="item-list__info">
      <div class="item-list__info-title">게이밍 PC 팝니다</div>
      <div class="item-list__info-meta">역삼동 19초 전</div>
      <div class="item-list__info-price">100만원</div>
   </div>
</div> */}

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

const renderData = (data) => {
   const main = document.querySelector("main");

   // reverse()   : 데이터를 거꾸로 바꾼다.
   data.reverse().forEach(async (obj) => {
      const div = document.createElement("div");
      div.className = 'item-list';

      const imgDiv = document.createElement("div");
      imgDiv.className = "item-list__img"

      const img = document.createElement("img");
      const res = await fetch(`/images/${obj.id}`);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      
      if(url) img.src = url;
      else img.src = 'assets/img.svg';

      const InfoDiv = document.createElement("div");
      InfoDiv.className = "item-list__info";

      const InfoTitleDiv = document.createElement("div");
      InfoTitleDiv.className = "item-list__info-title";
      InfoTitleDiv.innerText = obj.title;
      
      const InfoMetaDiv = document.createElement("div");
      InfoMetaDiv.className = "item-list__info-meta";
      InfoMetaDiv.innerText = obj.place + " " +calcTime(obj.insertAt);
      
      const InfoPriceDiv = document.createElement("div");
      InfoPriceDiv.className = "item-list__info-price";
      InfoPriceDiv.innerText = obj.price;

      imgDiv.appendChild(img);      
      InfoDiv.appendChild(InfoTitleDiv);
      InfoDiv.appendChild(InfoMetaDiv);
      InfoDiv.appendChild(InfoPriceDiv);
      div.appendChild(imgDiv);
      div.appendChild(InfoDiv);
      main.appendChild(div);
   });
};

const fetchList = async () => {
   const accessToken = window.localStorage.getItem("token");
   const res = await fetch('/items', {
      headers:{
         Authorization: `Bearer ${accessToken}`,
      },
   });

   if (res.status === 401) {
      alert("로그인이 필요합니다!");
      window.location.pathname = "/login.html";
      return
   }

   const data = await res.json();
   // console.log(data);
   renderData(data);
}

fetchList();