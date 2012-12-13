var oauth2_endpoints ={ 
	"Google":{
			"auth_endpoint":"https://accounts.google.com/o/oauth2/auth",
			"token_endpoint":"https://accounts.google.com/o/oauth2/token",
			"resource_endpoint":"https://www.googleapis.com/oauth2/v1",
			"redirect_uri": "http://authorizr.herokuapp.com/login/oauth2callback",
			"scope": "https://www.googleapis.com/auth/userinfo.profile ",
      "user_callback_page": "http://placehold.it/200%26text=Close+browser+now"
	},
	
	"Facebook":{
		 	"auth_endpoint" : "https://www.facebook.com/dialog/oauth",
	        "token_endpoint" : "https://graph.facebook.com/oauth/access_token",
	        "resource_endpoint" : "https://graph.facebook.com",
	        "redirect_uri": "http://authorizr.herokuapp.com/login/oauth2callback",
          "user_callback_page": "http://placehold.it/200%26text=Close+browser+now"  
	},
	"Stack exchange" : {	
		"auth_endpoint" : "https://stackexchange.com/oauth",
		"token_endpoint" : "https://stackexchange.com/oauth/access_token",
        "resource_endpoint" : "https://api.stackexchange.com/2.0",
        "redirect_uri": "http://authorizr.herokuapp.com/login/oauth2callback",
        "user_callback_page": "http://placehold.it/200%26text=Close+browser+now"
     },
  	"Foursquare" : {
        "auth_endpoint" : "https://foursquare.com/oauth2/authenticate",
        "token_endpoint" : "https://foursquare.com/oauth2/access_token",
        "resource_endpoint" : "https://api.foursquare.com/v2",
        "redirect_uri": "http://authorizr.herokuapp.com/login/oauth2callback",
        "user_callback_page": "http://placehold.it/200%26text=Close+browser+now" 		
  	},
  	"Github" : {
        "auth_endpoint" : "https://github.com/login/oauth/authorize",
        "token_endpoint" : "https://github.com/login/oauth/access_token",
        "resource_endpoint" : "https://api.github.com",
        "redirect_uri": "http://authorizr.herokuapp.com/login/oauth2callback",
        "user_callback_page": "http://placehold.it/200%26text=Close+browser+now"
     },
     "Instagram" : {
       	"auth_endpoint" : "https://api.instagram.com/oauth/authorize/",
        "token_endpoint" : "https://api.instagram.com/oauth/access_token",
        "resource_endpoint" : "https://api.instagram.com/v1",
        "redirect_uri": "http://authorizr.herokuapp.com/login/oauth2callback",
        "user_callback_page": "http://placehold.it/200%26text=Close+browser+now"
     }    
};



var oauth1_endpoints ={ 
	"Twitter":{
			"authorize_url":"https://api.twitter.com/oauth/authorize",			
			"user_callback_page": "http://placehold.it/200%26text=Close+browser+now",
      "request_token_endpoint": "https://api.twitter.com/oauth/request_token",
      "access_token_endpoint": "https://api.twitter.com/oauth/access_token"
	}
};

$(function() {

	//build menu
	for(var provider in oauth2_endpoints ){
  		$("#dropdownLinksOa2").append($('<li><a href="#'+provider+'">'+provider+'</a></li>'));
    }
	          
    $("#dropdownLinksOa2 a").click(function(event) {
    
    	event.preventDefault();
  		
  		key = $(this).attr('href').substring(1); 		  		   		
  		
  		endpoint = oauth2_endpoints[key];	    
  		     	
     	for(var k in endpoint ){	     
      		$("#id_oa2-"+k).val(endpoint[k]);
    	}
    });
    
    //build menu
	for(var provider in oauth1_endpoints ){
  		$("#dropdownLinksOa1").append($('<li><a href="#'+provider+'">'+provider+'</a></li>'));
    }
	          
    $("#dropdownLinksOa1 a").click(function(event) {
    
    	event.preventDefault();
  		
  		key = $(this).attr('href').substring(1); 		  		   		
  		
  		endpoint = oauth1_endpoints[key];	    
  		     	
     	for(var k in endpoint ){	     
      		$("#id_oa1-"+k).val(endpoint[k]);
    	}
    });
});
