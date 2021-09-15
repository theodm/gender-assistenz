<script lang="ts">
import {  ChangeSet, StateEffect } from '@codemirror/state';
import type {ChangeSpec} from '@codemirror/state';
import { RangeSet, RangeValue, Range } from '@codemirror/rangeset';
import { STATE_EFFECT_SET_POSSIBLE_CORRECTION_PREVIEW } from "./MarkChangesViewPlugin";

import type { EditorView } from '@codemirror/view';

    import {onMount} from 'svelte'
    
	import { createEventDispatcher } from 'svelte';
import { STATE_EFFECT_DONT_HIDE_TOOLTIP_INFO } from './InfoOccurencesTooltipField';
    import type { InfoOccurence, PossibleCorrection } from './MarkInfoOccurencesViewPlugin';
    import { STATE_EFFECT_REMOVE_INFO, STATE_EFFECT_TEMP_HIDE_INFO, STATE_EFFECT_TEMP_SHOW_INFO } from "./MarkInfoOccurencesViewPlugin"
    export let infoOccurence: InfoOccurence;
    export let editorView: EditorView;
    export let getConvertIntoGenderFormFn: () => (str: string) => string;

    let changeSetReverse: ChangeSet | null = null

    function reverseTemporaryChanges() {
      const effects: StateEffect<unknown>[] = [
        STATE_EFFECT_TEMP_SHOW_INFO.of(),
        STATE_EFFECT_SET_POSSIBLE_CORRECTION_PREVIEW.of(null),
        STATE_EFFECT_DONT_HIDE_TOOLTIP_INFO.of()
      ];

      if (changeSetReverse) {
        editorView.dispatch({
          changes: changeSetReverse,
          effects: effects
        })
        
        changeSetReverse = null;
      }
    }

    /**
     * Benutzer möchte einen Korrekturvorschlag übernehmen.
     */
    function onApplyCorrection(
      correction: PossibleCorrection
    ) {
      reverseTemporaryChanges();

      const effects: StateEffect<unknown>[] = [
        STATE_EFFECT_REMOVE_INFO.of(infoOccurence)
      ];

      const changes: ChangeSpec[] = []
      for (const change of correction.changes) {
        const iter = change._range!.iter();

        changes.push({
          from: iter.from,
          to: iter.to,
          insert: getConvertIntoGenderFormFn()(change.replace_with)
        });
      }

      const changeSet = editorView.state.changes(changes)

      editorView.dispatch({
        effects: effects,
        changes: changeSet
      })
    }


    function onMouseEnter(pc: PossibleCorrection) {
      reverseTemporaryChanges();

      const effects: StateEffect<unknown>[] = [
        STATE_EFFECT_TEMP_HIDE_INFO.of(),
        STATE_EFFECT_SET_POSSIBLE_CORRECTION_PREVIEW.of(pc),
        STATE_EFFECT_DONT_HIDE_TOOLTIP_INFO.of()
      ];
      
      const changes: ChangeSpec[] = []
      for (const change of pc.changes) {
        const iter = change._range!.iter();

        changes.push({
          from: iter.from,
          to: iter.to,
          insert: getConvertIntoGenderFormFn()(change.replace_with)
        });
      }

      const changeSet = editorView.state.changes(changes)

      changeSetReverse = changeSet.invert(editorView.state.doc);
      
      editorView.dispatch({
        changes: changeSet,
        effects: effects
      })


    }

    function onMouseLeave() {
      reverseTemporaryChanges();
    }

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
      {:else}
      <hr/>
      <div class="px-1 py-2 text">     
        <ul class="pl-3 text-sm list-decimal">
          {#each infoOccurence.possibleCorrections as pc}
          <li on:click={() => onApplyCorrection(pc)} 
            on:mouseenter={() => onMouseEnter(pc)}
            on:mouseleave={() => onMouseLeave()}
            >
            {#each pc.changes.filter(it => it.type === "NOUN") as change}
              {change.replace_with}  
            {/each}
          </li>
          {/each}
        </ul>
        </div>
      {/if}
  </div>
  