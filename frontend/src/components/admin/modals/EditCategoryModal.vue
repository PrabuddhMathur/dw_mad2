<template>
    <div class="modal fade" :id="category.cid + 'EditCategoryModal'">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Edit Category</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form method = "POST" action = "/edit/category/{{ category['cid'] }}">
                    <div class="modal-body">
                        <div class="form-floating mb-3">
                            <input name="CategoryName" :value="category.cname" type="text" class="form-control" placeholder="For Eg.: Spices" required>
                            <label for="CategoryName">Category Name</label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary">Save changes</button>
                    </div>
            </form>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
    export default {
        props: {
            category:{
                type: Object,
                required: true
            }
        }
    }
</script>