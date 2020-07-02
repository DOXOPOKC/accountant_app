<template lang="pug">
    v-dialog(
      v-model="commentsDialogState"
      max-width="600px"
    )
      template(
        v-slot:activator="{ on }"
      )
        v-btn(
          class="mr-2"
          icon
          v-on="on"
        )
          v-icon(small) mdi-comment
      v-card(
        outlined
      )
        v-card-title
          span(class="headline font-weight-light") Комментарии
          v-spacer
          v-btn(
            icon
            @click="commentsDialogState = false"
          )
            v-icon mdi-close
        v-card-text(class="pb-0")
            v-container(
              px-0 pb-0
            )
              v-row(
                v-if="!comments.length"
                no-gutters
                class="fill-height"
              )
                v-col(
                  cols="12"
                  justify="center"
                  align="center"
                  class="fill-height"
                )
                  v-chip(
                    :ripple="false"
                  )
                    | Здесь еще нет комментариев
              v-row(
                v-else
                no-gutters
              )
                v-col(
                  cols="12"
                )
                  v-list(
                  )
                    template(
                      v-for="(comment, index) in comments"
                    )
                      v-list-item(
                        :key="comment.id"
                        @click=""
                      )
                        v-list-item-content
                          v-list-item-title {{ comment.id }} - {{ comment.commentary_text }}
                          v-list-item-subtitle {{ comment.creation_date | dateFormat }}
                      v-divider
              v-row(
                no-gutters
                class="fill-height"
              )
                v-col(
                  cols="12"
                )
                  v-text-field(
                    type="text"
                    label="Добавить комментарий..."
                    v-model="commentText"
                    append-outer-icon="mdi-send"
                    @keyup.enter="sendMessage($event.target.value)"
                    @click:append-outer="sendMessage($event.target.value)"
                  )
</template>

<script>
import { mapState, mapActions } from 'vuex'
// import { ValidationProvider, ValidationObserver } from 'vee-validate'

export default {
  props: {
    viewState: {
      type: String,
      default: 'package',
      required: true
    },
    fileId: {
      type: Number,
      default: 1
    }
  },
  async fetch () {
    // eslint-disable-next-line no-console
    console.log(this.viewState)
    if (this.viewState === 'package') {
      await this.$store.dispatch('comments/FETCH_COMMENTS', {
        packageId: this.$route.params.packageId
      })
    } else {
      await this.$store.dispatch('comments/FETCH_FILE_COMMENTS', {
        packageId: this.$route.params.packageId,
        fileId: this.fileId
      })
    }
  },
  data: () => ({
    commentsDialogState: false,
    commentText: ''
  }),
  computed: {
    ...mapState({
      comments: state => state.comments.list
    })
  },
  methods: {
    ...mapActions({
      CREATE_COMMENT: 'comments/CREATE_COMMENT',
      FETCH_COMMENTS: 'comments/FETCH_COMMENTS',
      CREATE_FILE_COMMENT: 'comments/CREATE_FILE_COMMENT',
      FETCH_FILE_COMMENTS: 'comments/FETCH_FILE_COMMENTS'
    }),
    async sendMessage (comment) {
      if (this.viewState === 'package') {
        await this.CREATE_COMMENT({
          packageId: this.$route.params.packageId,
          comment
        })
      } else {
        await this.CREATE_FILE_COMMENT({
          packageId: this.$route.params.packageId,
          fileId: this.fileId,
          comment
        })
      }
      this.commentText = ''
    }
  }
}
</script>

<style>

</style>
