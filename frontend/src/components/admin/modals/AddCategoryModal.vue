<template>
    <div class="modal fade" id="AddCategoryModal">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Add Category</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form method = "POST" action = "/create/category">
                    <div class="modal-body">
                        <div class="form-floating mb-3">
                            <input name="CategoryName" type="text" class="form-control" id="CategoryName" placeholder="For Eg.: Spices" required>
                            <label for="CategoryName">Category Name</label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>