
// nav-links
menu = document.getElementById('side-menu')


//#region heistform
// get heistform
form = document.querySelector('form.heist_form')
imageFields = form.querySelectorAll('p:has(input[accept="image/*"])')
selectFields = form.querySelectorAll('p:has(select)')

if (imageFields) {
   if (form.classList.contains('update_form')) {
      imageFields.forEach(field => {
      anchor = field.querySelector('a')
      image = document.createElement('img')
      image.src = anchor.href
      anchor.innerHTML = ''
      anchor.appendChild(image)

      basediv = document.createElement('div')
      basediv.classList.add('grid')
      div1 = document.createElement('div')
      div2 = document.createElement('div')

      nodes = field.childNodes
      
      div1.appendChild(nodes.item(2))
      div1.appendChild(nodes.item(2))
      div2.appendChild(nodes.item(3))
      div2.appendChild(nodes.item(3))

      
      basediv.appendChild(div1)
      basediv.appendChild(div2)
      field.appendChild(basediv)
      
      field.querySelector('br').style.display = 'none'
   });
   }

}

if (selectFields) {
   selectFields.forEach(element => {
      select_field = element.querySelector('select')
      options = select_field.querySelectorAll('option')
      new_div = document.createElement('div')
      new_div.classList.add('flex')
      
      options.forEach(element => {
         option_span = document.createElement('span')
         option_span.setAttribute("id", element.value)
         option_span.innerHTML = element.innerHTML
         if (element.selected) {
            option_span.classList.add('selected')
         }
         option_span.addEventListener('click', (pointer) => {
            select_active = pointer.target.parentElement.parentElement.querySelector('select')
            id = pointer.target.id
            // select_active.selectByValue(id)
            if (select_active.multiple) {
               select_active.querySelectorAll('option').forEach(option => {
                  // console.log(option.value);
                  if (option.value == id) {
                     if (option.selected) {
                        option.selected = false
                        option.removeAttribute('selected')
                        pointer.target.classList.remove('selected')
                     } else {
                        option.selected = true
                        option.setAttribute('selected','')
                        pointer.target.classList.add('selected')
                     }
                  }
               });
            } else {
               console.log('Not yet done');
            }
            // console.log(select_active.multiple);
         })
         new_div.appendChild(option_span)
      });
      
      element.appendChild(new_div)
   });
}

//#endregion

