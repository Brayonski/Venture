$(document).ready(function(){    
     $(function(){
        $('#menu').slicknav({
            'prependTo':'nav',
        });
    });
	
	$('#slideclick').click(function(){
		$('#slidetoggle').slideToggle();
		return false;
	});
});