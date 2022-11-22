<template>
<div class="jumbotron vertical-center">
  <div class="container">
    
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css" integrity="sha384-9+PGKSqjRdkeAU7Eu4nkJU8RFaH8ace8HGXnkiKMP9I9Te0GJ4/km3L1Z8tXigpG" crossorigin="anonymous">
    <div class="row">
      <div class="col-sm-12 ">
       <h1>Card List</h1>
        <hr><br>

       <b-alert variant="success" v-if="showMessage" show> {{ message }} </b-alert>

        <button type="button" class="btn btn-success btn-sm" v-b-modal.card-modal>Add Card</button>
        <table>
          <thead>
            <tr>
              <th><h3>Title</h3></th>
              <th><h3>Content</h3></th>
              <th><h3>card id</h3></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(card, index) in cards" :key="index">
              <td>{{card.title}}</td>
              <td>{{card.content}}</td>
              <td>{{card.card_id}}</td>
              <div class="btn-group" role="group">
                <button
                    type="button"
                    class="btn btn-info btn-sm"
                    v-b-modal.card-update-modal
                    @click="editCard(card)"> Update </button>
                <button type="button" class="btn btn-danger btn-sm" @click="deleteCard(card)">Delete</button>
              </div>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addCardModal"
         id="card-modal"
         title="Add a new card" hide-backdrop
         hide-footer
         >
      <b-form @submit="onSubmit" @reset="onReset">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">

        <b-form-input id="form-title-input"
                      type="text"
                      v-model="addCardForm.title"
                      required
                      placeholder="Enter title">
        </b-form-input>
      </b-form-group>

      <b-form-group id="form-content-group"
                    label="Content:"
                    label-for="form-content-input">
            <b-form-input id="form-content-input"
                          type="text"
                          v-model="addCardForm.content"
                          required
                          placeholder="Enter content">
          </b-form-input>
        </b-form-group>

        <b-button type="submit" variant="outline-info">Submit</b-button>
        <b-button type="reset" variant="outline-danger">Reset</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="editCardModal"
         id="card-update-modal"
         title="Update" hide-backdrop
         hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        
      <b-form-group id="form-title-edit-group"
                    label="Title:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>

        <b-form-group id="form-content-edit-group"
                      label="Content:"
                      label-for="form-content-edit-input">
            <b-form-input id="form-content-edit-input"
                          type="text"
                          v-model="editForm.content"
                          required
                          placeholder="Enter content">
            </b-form-input>
          </b-form-group>

        <b-button-group>
          <b-button type="submit" variant="outline-info">Update</b-button>
          <b-button type="reset" variant="outline-danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</div>
</template>



<script>
  import axios from 'axios';
  export default {
    data() {
      return {
        cards: [],
        addCardForm: {
          title: '',
          content: '',
        },
        editForm: {
          title: '',    
          content: '',
        },
      };
    },
    message:'',
    methods: {
        getCards() {
          const path = 'http://127.0.0.1:5000/cards';
          axios.get(path)
            .then((res) => {
              this.cards = res.data.cards;
            })
            .catch((error) => {
              console.error(error);
            });
        },

        addCard(payload) {
          const path = 'http://127.0.0.1:5000/cards';
          axios.post(path, payload)
            .then(() => {
              this.getCards();
              
              // for message alert
              this.message = 'Card added 🕹️ !';
              
              // to show message when is added
              this.showMessage = true;
      
            })
            .catch((error) => {
              console.log(error);
              this.getCards();
            });
        },

        initForm() {
          this.addCardForm.title = '';
          this.addCardForm.content = '';

          this.editForm.title = '';
          this.editForm.content = '';
        }, 

        onSubmit(e) {
          e.preventDefault();
          this.$refs.addCardModal.hide();

          const payload = {
            title: this.addCardForm.title,
            content: this.addCardForm.content, 
          };

          this.addCard(payload);
          this.initForm();
        },

        onSubmitUpdate(e) {
          e.preventDefault();
          this.$refs.editCardModal.hide();

          const payload = {
            title: this.editForm.title,
            content: this.editForm.content,
          };
          this.updateCard(payload, this.editForm.id);
        },

        onReset(e) {
          e.preventDefault();
          this.$refs.addCardModal.hide();
          this.initForm();
        },

        updateCard(payload, cardID) {
          const path = `http://localhost:5000/cards/${cardID}/update`;
          axios.put(path, payload)    
            .then(() => {
              this.getCards();
              this.message = 'card updated ⚙️!';
              this.showMessage =  true;
            })
            .catch((error) => {
              console.error(error);
              this.getCards();
            });
        },
        // Handle Update Button 
        editCard(card) {
          this.editForm = card;
        },
        // 5 Handle reset / cancel button click
        onResetUpdate(e) {
          e.preventDefault();
          this.$refs.editCardModal.hide();
          this.initForm();
          this.getCards(); 
        },

        removeCard(cardID) {
          const path = `http://localhost:5000/cards/${cardID}/delete`;
          axios.delete(path)
            .then(() => {
              this.getCards();
              this.message = 'card Removed 🗑️!';
              this.showMessage = true;
            })
            .catch((error) => {
              // eslint-disable-next-line
              console.error(error);
              this.getCards();
            });
        },


        deleteCard(card) {
          this.removeCard(card.card_id);
        },

      },
    created() {
      this.getCards(); 
    },
  };
</script>