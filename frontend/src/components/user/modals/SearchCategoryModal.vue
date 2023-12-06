<template>
    <div class="modal fade" id="SearchCategoryModal">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Search Category</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form method = "POST" action = "/search_category">
                    <div class="modal-body">
                        <div class="form-floating mb-3">
                            <input name="category" type="search" class="form-control" id="category" list="search category" placeholder="For Eg.: Spices" required>
                            <datalist id="search category">
                                <!-- {% for category in categories %} -->
                                <!-- <option value="{{ category['cname'] }}"> -->
                                <!-- {% endfor %} -->
                            </datalist>
                            <label for="category">Category Name</label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary">Search</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
    export default {
        
}
</script>