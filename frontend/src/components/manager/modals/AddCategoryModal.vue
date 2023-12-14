<template>
    <div class="modal fade" id="AddCategoryModal">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Request Category</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form>
                    <div class="modal-body">
                        <div class="form-floating mb-3">
                            <input v-model="cname" name="CategoryName" type="text" class="form-control" id="CategoryName" placeholder="For Eg.: Spices" required>
                            <label for="CategoryName">Category Name</label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button @click="addCategoryRequest()" type="submit" class="btn btn-primary">Submit Request</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
    export default {
        data(){
            return {
                cname:"",
            }
        },
        methods:{
            async addCategoryRequest(){
                await axios
                .post("http://127.0.0.1:1430/manager-api/approval/category",{
                    request_type:"add",
                    cname:this.cname
                })
                .then((response)=>response.data)
                .then((response)=>{alert(response)})
            }
        }
    }
</script>