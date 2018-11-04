(function() {
  'use strict';

   var nav_btn = document.getElementById('nav_btn');
   var nav = document.getElementById("navi");
   var nav_flag = 0

   nav_btn.addEventListener('click', function() {
       if(nav_flag==0){
           nav.classList.remove("display-none");
           nav_flag = 1;
       }else{
           nav.classList.add("display-none");
           nav_flag = 0;
       }
   });


   var search_btn = document.getElementById('search_btn');
   var search = document.getElementById("search");
   var search_flag = 0

   search_btn.addEventListener('click', function() {
       if(search_flag==0){
           search.classList.remove("display-none");
           search_flag = 1;
       }else{
           search.classList.add("display-none");
           search_flag = 0;
       }
   });

})();
