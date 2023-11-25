
export default () => ({
    facilitators: {},
    services: {},
    active_service: {},
    unavailable: [],
    update_path: '{% url 'api:update-facilitators' %}',
    update_ready: false,
    csrf() {
        token = document.getElementById('token').firstElementChild.value;
        return token;
    },
    async init(){
        // get the services =======================
        this.services = await getServices('{% url 'api:get-service-lists' stat.pk %}')
        // get the facilitators ===================
        this.facilitators = await getFacilitators('{% url 'api:facilitators' %}')
        // set the default active service ====================
        this.active_service = this.services[0]

        this.setLists()
    },
    setLists(){
        this.unavailable = []
        for (const i in this.facilitators) {
            let current = this.facilitators[i]
            let actives = this.active_service.facilitators

            let is_active = actives.find((value) => {
                return value.id == current.id
            })

            if (!is_active){
                let isThere = this.unavailable.find((value) => {
                    return value.id == current.id
                })
                // if current not in the unavailable array add it there
                if (!isThere){
                    this.unavailable.push(current)
                }
            }
        }
    },
    handleCheck(facilitator, isAvailable){
        this.update_ready = false
        let class_list = document.querySelector(`input#check${facilitator.id}`).classList
        if (class_list.contains('checked'))
            class_list.remove('checked')
        else
            class_list.add('checked')
        setTimeout(() => {
            this.update_ready = CheckActions(facilitator, isAvailable, this.active_service.facilitators, this.unavailable)
        }, 300)
        // send updates to database
        this.update()
    },
    update(){
        setInterval(() => {
            if (this.update_ready){
                console.log('Saving....')

                const response = udpadeFacilitators(this.update_path, this.active_service, this.csrf())
                
                console.log(response)
                this.update_ready = false
                return
            }
            else
                console.log('waiting to save')
        }, 2000)
    }
})