<template lang="pug">
  section
    h1(class="header") Nuxt TypeScript Starter
    div(class="cards")
      Card(
        v-for="person in people"
        :key="person.id"
        :person="person"
      )
      v-content
        v-row(justify="center")
          v-col(cols="4")
            v-card(flat)
              v-card-title(class="subtitle-1")
                | Headline
              v-card-text {{questions}}
              v-card-actions
</template>

<script lang="ts">
import {
  Component,
  Vue
} from "nuxt-property-decorator"
import { State } from "vuex-class"
import { Person } from "~/types";
import Card from "~/components/Card.vue"

interface Question {
  title: string,
}

@Component({
  components: {
    Card
  }
})
export default class extends Vue {
  @State people!: Person;
  questions: Question[] = [ {title: "123"}, {title: "123"} ];
}
</script>
