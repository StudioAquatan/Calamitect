(function() {
  'use strict';


   var category_search= document.getElementById('category-search');
   var category_search_menu= document.getElementById('category_search-menu');
   var category_search_flag = 0

   category_search.addEventListener('click', function() {
       if(category_search_flag==0){
           category_search_menu.classList.remove("display-none");
           category_search_flag = 1;
       }else{
           category_search_menu.classList.add("display-none");
           category_search_flag = 0;
       }
   });

})();
