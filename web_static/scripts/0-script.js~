#!/usr/bin/node

$(document).ready(function() {
  // Function to add numbered input fields for ingredients
  $('#addIngredient').click(function(e) {
    e.preventDefault();
    var count = $('#ingredients-list div').length + 1;
    $('#ingredients-list').append('<div><label for="ingredient_' + count + '">Ingredient ' + count + ':</label><input type="text" id="ingredient_' + count + '" name="ingredient_' + count + '" required><br></div>');
  });

  // Function to add numbered textarea fields for instructions
  $('#addInstruction').click(function(e) {
    e.preventDefault();
    var count = $('#instructions-list textarea').length + 1;
    $('#instructions-list').append('<div><label for="instruction_' + count + '">Instruction ' + count + ':</label><textarea id="instruction_' + count + '" name="instruction_' + count + '" rows="4" cols="50" required></textarea><br></div>');
  });
});
