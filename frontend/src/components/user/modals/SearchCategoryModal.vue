<template>
    <div class="modal fade" id="SearchCategoryModal">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Search Category</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form @submit.prevent="searchCategories">
                    <div class="modal-body" >
                        <div class="form-floating mb-3">
                            <input v-model="category" name="category" type="search" class="form-control" id="category" list="search category" placeholder="For Eg.: Spices" required>
                            <datalist id="search category" >
                                <span v-for="category in categories"  :key="category.cid">
                                    <option :value="category.cname" />
                                </span>
                            </datalist>
                            <label for="category">Category Name</label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" data-bs-dismiss="modal" class="btn btn-primary">Search</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            categories:{
                type:Object,
                required:true
            }
        },
        data(){
            return{
                userSession: JSON.parse(localStorage.getItem("userSession")) || null,
                category:'',
                showModal: false,
            }
        },
        methods:{
            searchCategories(){
                if (this.userSession){          
                    this.$router.push({name:"search",query:{search_by:'category',q:this.category}})
                }else{
                    alert("Please login and try again!")
                }
            }
        }
}
</script>