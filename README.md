Suggestit Search Suggestions
=============================

This is a simple search suggestions engine written in web.py and using redis+memcached.

It has an endpoint for /set/ which basically sets a certain term and breaks it down for storage. Therefore, if you store 'get married in vegas' - it will break this phrase down and store it as sub phrases. The engine will also rank suggestions based on how often they are hit by using redis sets. That way, the most commonly searched items bubble to the top of the suggestions list.

You must *not* make your /set/ endpoint web accessible. Try to keep it secure to prevent people from messing with your search suggestions.

The /get/ endpoint is simple. Once you store a word, say "super" into the engine. If you make a request to /get/?term=s it will return "super" as a suggestion.

Google's research showed that search suggestions should return in under 400ms to feel fast enough. I'm running this on a system with over 10 million keys and the suggestions come back in well under 400ms (with network latency accounted for).

The /get/ endpoint can easily be used with [jQuery UI's autocomplete feature](http://jqueryui.com/autocomplete/).

 	$(function() {		
 		$( "#searchbox").autocomplete({
 			source: '/suggestit/get/',
 			select: function(event, ui) {
                     if(ui.item){
                         $(this).val(ui.item.value);
                     }
                     $(this).parents("form").submit();
                 }
 		});
 	});

The suggestion engine returns results in JSON ranked by popularity.

You can run it using:
	python suggest.py

In production however, it's best to run it through uWSGI or another WSGI server.