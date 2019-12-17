<template lang="pug">
  v-card
    v-card-title(class="headline") {{person.first_name}}
</template>

<script lang="ts">
import { Component, Prop, Vue } from "nuxt-property-decorator"
import { Person } from "~/types"

@Component({})
export default class Card extends Vue {
  @Prop() person!: Person
}
</script>
