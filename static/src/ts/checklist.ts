// get all facilitators
// get all services for date
// get all active facilitators
// get all inactive facilitators
// update service

type Service = {
    id: number;
    name: string;
    junior: number;
    senior: number;
    first_time_visitors: number;
    salvations: number;
    non_system_facilitators: number;
    facilitators_available: number[];
};
type Facilitator = {
    id: number;
    name: string;
    active: boolean;
    only_in_band: boolean;
    gender: string;
};



export default (): any => ({
    facilitators: [],
    services: [],
    updateTimer: null,
    servicesUrl: '',
    editMode: false,
    statsLoader: false,

    async initialize(pk: number, servicesUrl: string, facilitatorsUrl: string){
        this.servicesUrl = servicesUrl
        // Modify the URL to include the stat_id query parameter
        const servicesWithStatUrl = `${servicesUrl}?stat_id=${pk}&format=json`
        this.services = await this.getServices(servicesWithStatUrl)
        this.facilitators = await this.getFacilitators(facilitatorsUrl)
    },

    handleCheck(facilitator: Facilitator, serviceId: number){
        const service = this.services.find((s:Service) => s.id === serviceId);
        if (service) {
            const index = service.facilitators_available.indexOf(facilitator.id);
            if (index > -1) {
                // Remove facilitator if already present
                service.facilitators_available.splice(index, 1);
            } else {
                // Add facilitator if not present
                service.facilitators_available.push(facilitator.id);
            }
            // Trigger a re-render
            this.services = [...this.services];
            
            // Call the debounced update function
            this.debouncedUpdateServices();
        }
    },

    debouncedUpdateServices() {
        if (this.updateTimer) {
            clearTimeout(this.updateTimer);
        }
        this.updateTimer = setTimeout(() => {
            this.updateServices();
        }, 2000);
    },

    async updateServices() {
        this.statsLoader = true
        try {
            // Get the CSRF token from the cookie
            const csrftoken = this.getCookie('csrftoken');

            const response = await fetch(this.servicesUrl, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify(this.services),
            });
            if (!response.ok) {
                throw new Error('Failed to update services');
            }
            console.log('Services updated successfully');
        } catch (error) {
            console.error('Error updating services:', error);
        }
        this.statsLoader = false
    },

    // Get total number of male facilitators for a specific service
    getMaleFacilitatorsCount(service: Service) {
        return this.facilitators.filter((f: Facilitator) => 
            service.facilitators_available.includes(f.id) && f.gender.toLowerCase() === 'm'
        ).length;
    },

    // Get total number of female facilitators for a specific service
    getFemaleFacilitatorsCount(service: Service) {
        return this.facilitators.filter((f: Facilitator) => 
            service.facilitators_available.includes(f.id) && f.gender.toLowerCase() === 'f'
        ).length;
    },

    getAllFacilitatorIds():Set<number> {
        const userIds = new Set<number>();
        this.services.forEach((service: Service) => {
            service.facilitators_available.forEach((id: number) => {
                userIds.add(id)
            })
        });
        return userIds
    },

    getPresentFacilitators() {
        const ids:Set<number> = this.getAllFacilitatorIds()
        const facilitators:Set<Facilitator> = new Set()

        for (const id of ids) {
            const facilitatorLs = this.facilitators.filter((f: Facilitator) => f.id == id)
            facilitators.add(facilitatorLs[0])
        }

        return facilitators
    },

    getPresentFacilitatorsTotal() {
        return this.getAllFacilitatorIds().size
    },

    // Helper function to get CSRF token from cookie
    getCookie(name: string) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    // getting data
    async getFacilitators(url: string){ 
        url = `${url}?format=json`

        const response = await fetch(url)
        return await response.json();
    },
    async getServices(url: string){
        const response = await fetch(url)
        return await response.json();
    }
})
