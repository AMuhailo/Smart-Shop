const field = document.querySelector('.form-number')
window.addEventListener('click',function (event) {
    if (event.target.dataset.action == 'minus' && field.value > 1){
        field.value = --field.value
    } 
    if (event.target.dataset.action == 'plus'){
        field.value = ++field.value
    }

})

const tab = document.querySelectorAll('[data-tab]')
const content = document.querySelectorAll('[data-tab-content]')
tab.forEach((item)=>{
    item.addEventListener('click', function () {
        const thisTab = this.dataset.tab
        const contentTab = document.querySelector("#"+`${thisTab}`)
        content.forEach((item)=>{
            item.classList.add('hidden')
        })
        contentTab.classList.remove('hidden')
        tab.forEach((item)=>{
            item.classList.remove('active-tab')
        })
        item.classList.add('active-tab')
    })
})