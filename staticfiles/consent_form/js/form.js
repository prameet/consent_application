
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
    $(document).ready(function() {
        $('#consent-form').submit(function(e) {
            e.preventDefault();
            var formData = new FormData(this);
            alert('here');
        });
    });
</script>