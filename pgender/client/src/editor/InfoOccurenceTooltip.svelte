<script lang="ts">
    import {onMount} from 'svelte'
    
	import { createEventDispatcher } from 'svelte';
    import type { InfoOccurence } from './MarkInfoOccurencesViewPlugin';
  
    export let infoOccurence: InfoOccurence;

  </script>
  
  <style>
  
  </style>
  
  <div class="px-2 bg-gray-100 border border-black">
      <div class="flex items-center px-2 py-2">
        {#if infoOccurence.shouldBeGendered}
            <div class="w-2 h-2 mr-3 bg-blue-400 border border-black"/>
            <div class="text-sm">Korrektur erforderlich</div>
        {:else}
            <div class="w-2 h-2 mr-3 bg-gray-400 border border-black"/>
            <div class="text-sm">Korrektur nicht erforderlich</div>
        {/if}
      </div>
      {#if !(infoOccurence.shouldBeGendered)} 
      <hr/> 
      <div class="px-1 py-2 text">     
        <ul class="pl-3 text-sm list-decimal">
          {#each infoOccurence.reasonNotGendered as rng}
            <li>{rng[1]}</li>
          {/each}
        </ul>
        </div>
      {/if}
  </div>
  