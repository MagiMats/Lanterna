<template>
<div class="jumbotron vertical-center">
  <div class="container">
    
    <div class="row">
      <div class="col-sm-12 ">
       <h1>Card List</h1>
        <hr><br>

        <button type="button" class="btn btn-success btn-sm" v-b-modal.card-modal>Add Card</button>
        <table>
          <thead>
            <tr>
              <th><h3>Title</h3></th>
              <th><h3>Content</h3></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(card, index) in cards" :key="index">
              <td>{{card.title}}</td>
              <td>{{card.content}}</td>
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

        addGame(payload) {
          const path = 'http://localhost:5000/cards';
          axios.post(path, payload)
            .then(() => {
              this.getCards();
              
              // for message alert
              this.message = 'Card added 🕹️ !';
              
              // to show message when game is added
              this.showMessage = true;
      
            })
            .catch((error) => {
              console.log(error);
              this.getCards();
            });
        },

        initForm() {
          this.addCardForm.title = '';
          this.addCardForm.genre = '';
        }, 

        onSubmit(e) {
          e.preventDefault();
          this.$refs.addCardModal.hide();

          const payload = {
            title: this.addCardForm.title,
            genre: this.addCardForm.content, 
          };
          this.addGame(payload);
          this.initForm();
        },

        onReset(e) {
          e.preventDefault();
          this.$refs.addCardModal.hide();
          this.initForm();
        },

      },
    created() {
      this.getCards(); 
    },
  };
</script>