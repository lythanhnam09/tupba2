class GestureDetector {
    constructor(selector, option = {
            mouseDown: null, 
            mouseMove: null, 
            mouseUp: null
        }, region = document.body) {
        this.region = region;
        this.e = document.querySelector(selector);
        this.e.draggable = false;
        this.useTouch = false;
        this.down = false;
        this.onMouseDown = option.mouseDown;
        this.onMouseMove = option.mouseMove;
        this.onMouseUp = option.mouseUp;
        this.lastpos = null;
        this.orgPos = {x:0,y:0};
        this.currentPos = {x:0,y:0};
        this.registerEvent();
    }

    registerEvent() {
        this.e.addEventListener('mousedown', event => {
            if (this.useTouch) return;
            if (event.button == 0) {
                this.downEvent(event.clientX, event.clientY);
                if (this.onMouseDown) this.onMouseDown(this, this.currentPos);
            }
        }, false);
        this.e.addEventListener('mousemove', event => {
            if (this.useTouch) return;
            if (this.down) {
                this.moveEvent(event.clientX, event.clientY);
                if (this.onMouseMove) this.onMouseMove(this, this.currentPos);
            }
        }, false);
        this.e.addEventListener('mouseup', event => {
            if (this.useTouch) return;
            if (event.button == 0) {
                this.upEvent(event.clientX, event.clientY);
                if (this.onMouseUp) this.onMouseUp(this, this.currentPos);
            }
        }, false);

        this.e.addEventListener('touchstart', event => {
            document.body.style.overflowY = "hidden";
            this.useTouch = true;
            this.downEvent(event.changedTouches[0].clientX, event.changedTouches[0].clientY);
            if (this.onMouseDown) this.onMouseDown(this, this.currentPos);
        }, false);
        this.e.addEventListener('touchmove', event => {
            if (this.down) {
                this.moveEvent(event.changedTouches[0].clientX, event.changedTouches[0].clientY);
                if (this.onMouseMove) this.onMouseMove(this, this.currentPos);
            }
        }, false);
        this.e.addEventListener('touchend', event => {
            document.body.style.overflowY = "unset";
            this.useTouch = false;
            this.upEvent(event.changedTouches[0].clientX, event.changedTouches[0].clientY);
            if (this.onMouseUp) this.onMouseUp(this, this.currentPos);
        }, false);
    }

    getMousePos(x, y) {
        return {x:x + document.documentElement.scrollLeft, y:y + document.documentElement.scrollTop};
    }

    updatePos(x, y) {
        this.lastpos = this.currentPos;
        this.currentPos = this.getMousePos(x, y);
    }

    downEvent(x, y) {
        this.region.style.touchAction = 'none';
        this.lastpos = this.currentPos = this.orgPos = this.getMousePos(x, y);
        this.down = true;
    }

    moveEvent(x, y) {
        // this.e.draggable = "false";
        this.updatePos(x, y);
    }

    upEvent(x, y) {
        this.region.style.touchAction = 'unset';
        this.orgPos = {x:x + document.documentElement.scrollLeft, y:y + document.documentElement.scrollTop};
        this.currentPos = this.orgPos;
        this.down = false;
    }

    get distance() {
        return {x: this.currentPos.x - this.orgPos.x, y: this.currentPos.y - this.orgPos.y};
    }

    get delta() {
        return {x: this.currentPos.x - this.lastpos.x, y: this.currentPos.y - this.lastpos.y};
    }
}

class SwipeScrollbar extends GestureDetector {
    constructor(selector, option = {
        mouseDown: null, 
        mouseMove: null, 
        mouseUp: null,
        min: 0,
        max: 100,
        value: 0,
        scale: 1
    }, region = document.body) {

        super(selector, option, region);
        this.min = option.min;
        this.max = option.max;
        this.value = option.value;
        this.scale = option.scale;
    }

    increase(num) {
        this.value += num;
        if (this.value > this.max) this.value = this.max;
        if (this.value < this.min) this.value = this.min;
    }

    moveEvent(x, y) {
        super.moveEvent(x, y);
        this.increase((this.currentPos.x - this.lastpos.x) * this.scale);
    }
}

class Draggable extends GestureDetector {
    constructor(selector, option = {
        mouseDown: null, 
        mouseMove: null, 
        mouseUp: null,
        lockX: false,
        lockY: false,
    }, region = document.body) {

        super(selector, option, region);
        this.lockX = option.lockX;
        this.lockY = option.lockY;
    }

    moveElement(dx, dy) {
        let left = this.e.offsetLeft + dx;
        let top = this.e.offsetTop + dy;
        if (! this.lockY) this.e.style.top = top + 'px';
        if (! this.lockX) this.e.style.left = left + 'px';
    }

    moveEvent(x, y) {
        // this.e.draggable = "false";
        super.moveEvent(x,y);
        let d = this.delta;
        this.moveElement(d.x, d.y);
    }
}