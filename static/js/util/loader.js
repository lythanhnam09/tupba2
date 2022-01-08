class Queue {
    constructor() {
        this.data = [];
    }

    enqueue(data) {
        this.data.push(data);
    }

    dequeue() {
        if (this.data.length <= 0) return null;
        let el = this.data[0];
        this.data.splice(0, 1);
        return el;
    }

    doLimit(limit) {
        if (this.data.length > limit) {
            let count = this.data.length - limit;
            for (let i=0;i<count;i++) this.dequeue();
        }
    }

    get length() {
        return this.data.length;
    }
}

class PagePreLoader {
    constructor(perpage, request, range = 1, cacheSize = 4) {
        // request: function(page, perpage) -> Future<Page>
        this.page = 1;
        this.perpage = perpage;
        this.request = request;
        this.range = range;
        this.pageCount = 1;
        this.cacheSize = cacheSize;
        this.pageData = new Queue();
    }

    checkPageLoaded(page, perpage) {
        for (let pg of this.pageData.data) {
            if (page == pg.page_num && perpage == pg.per_page) return pg;
        }
        return null;
    }

    async doRequest(page, perpage) {
        // console.log(`Loading page ${page}...`);
        let result = this.checkPageLoaded(page, perpage);
        if (! result) {
            let data = await this.request(page, perpage);
            this.receiveData(data);
            return data;
        }
        // console.log(`Page ${page} already loaded`);
        return result;
    }

    receiveData(data) {
        // console.log(data);
        // console.log(`Page ${data.page_num} received`);
        this.pageCount = data.page_count;
        this.pageData.enqueue(data);
        this.pageData.doLimit(this.cacheSize);
        // console.log(this.pageData.data);
    }

    async get(page) {
        // console.log(` * Requesting page ${page}...`);
        this.page = page;
        let result = await this.doRequest(page, this.perpage);
        for (let i=1;i<=this.range;i++) {
            if (page + i <= this.pageCount) this.doRequest(page + i, this.perpage);
            if (page - i >= 1) this.doRequest(page - i, this.perpage);
        }
        // console.log(`Done`);
        return result;
    }
}