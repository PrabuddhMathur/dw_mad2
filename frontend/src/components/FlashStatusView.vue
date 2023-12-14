<template>
    <div class="container-fluid">
        <div class="container" align="center">
            <!-- {% with messages=get_flashed_messages(with_categories=true) %} -->
            <!-- {% if messages %} -->
                    <!-- {% for category, message in messages %}         -->
                    <!-- {% if category == 'error' %} -->
                        <div class="alert alert-danger alter-dismissable fade show w-50" role="alert">
                            <div class="row">
                                <p class="col-11 m-0">{{ message }}</p>
                                <button type="button" class="btn-close col-1" data-bs-dismiss="alert" aria-label="Close"></button>
                            </div>
                        </div>
                    <!-- {% else %} -->
                        <div class="alert alert-success alter-dismissable fade show w-50" role="alert">
                            <div class="row">
                                <p class="col-11 m-0">{{ message }}</p>
                                <button type="button" class="btn-close col-1" data-bs-dismiss="alert" aria-label="Close"></button>
                            </div>
                        </div>
                    <!-- {% endif %} -->
                    <!-- {% endfor %}
            {% endif %}
            {% endwith %} -->
        </div>
    </div>
</template>
<script>
    export default {
        props: {
            category:{
                type: Object,
                required: true
            }
        }
    }
</script>