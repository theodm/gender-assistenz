<script lang="ts">
  import {onMount} from 'svelte'
  import Editor from './editor/Editor.svelte'
  import axios from "axios";
import type { InfoOccurence } from './editor/MarkInfoOccurencesViewPlugin';

  let analyzeResult: null | AnalyzeResult = null;

  interface AnalyzeResult {
    text: string;
    infos: Array<InfoOccurence>;
  }

  async function analyze(text: string) {
    const result = (
      await axios.post("http://localhost:8080/analyze", text)
    ).data;

    console.log(result);

    analyzeResult = result;
  }

</script>

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
  }

</style>

<div class="w-full h-screen p-4 App">
  <div class="text-xl text-center">Korrektur-Tool für gendergerechte Sprache</div>

  <div class="flex py-2">
    <button on:click={() => analyze(window.getEditorContent())} class="flex items-center px-4 py-2 font-bold text-white align-middle bg-blue-500 rounded hover:bg-blue-700">
      <!-- <div class="w-2 h-2 mr-2 bg-white"></div> -->
      Überprüfen
    </button>
  </div>
  <div class="flex justify-center w-full py-2 align-middle h-5/6">
      <Editor infos={analyzeResult ? analyzeResult.infos : []} class="w-full"/>
  </div>
</div>
