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
            // return false;
        });
        this.e.addEventListener('mousemove', event => {
            if (this.useTouch) return;
            if (this.down) {
                this.moveEvent(event.clientX, event.clientY);
                if (this.onMouseMove) this.onMouseMove(this, this.currentPos);
            }
            // return false;
        });
        this.e.addEventListener('mouseup', event => {
            if (this.useTouch) return;
            if (event.button == 0) {
                this.upEvent(event.clientX, event.clientY);
                if (this.onMouseUp) this.onMouseUp(this, this.currentPos);
            }
            // return false;
        });

        this.e.addEventListener('touchstart', event => {
            document.body.style.overflowY = "hidden";
            this.useTouch = true;
            this.downEvent(event.changedTouches[0].clientX, event.changedTouches[0].clientY);
            if (this.onMouseDown) this.onMouseDown(this, this.currentPos);
            // return false;
        });
        this.e.addEventListener('touchmove', event => {
            if (this.down) {
                this.moveEvent(event.changedTouches[0].clientX, event.changedTouches[0].clientY);
                if (this.onMouseMove) this.onMouseMove(this, this.currentPos);
            }
            // return false;
        });
        this.e.addEventListener('touchend', event => {
            document.body.style.overflowY = "unset";
            this.useTouch = false;
            this.upEvent(event.changedTouches[0].clientX, event.changedTouches[0].clientY);
            if (this.onMouseUp) this.onMouseUp(this, this.currentPos);
            // return false;
        });
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
        relative: false,
    }, region = document.body) {

        super(selector, option, region);
        this.lockX = option.lockX;
        this.lockY = option.lockY;
        this.relative = option.relative;
    }

    setPos(x, y) {
        this.e.style.left = x + 'px';
        this.e.style.top = y + 'px';
    }

    moveElement(dx, dy) {
        if (this.relative) {
            let stop = this.e.style.top == '' ? 0:parseFloat(this.e.style.top.substr(0, this.e.style.top.length - 2));
            let sleft = this.e.style.left == '' ? 0:parseFloat(this.e.style.left.substr(0, this.e.style.left.length - 2));
            let left = sleft + dx;
            let top = stop + dy;
            if (! this.lockY) this.e.style.top = top + 'px';
            if (! this.lockX) this.e.style.left = left + 'px';
        } else {
            let left = this.e.offsetLeft + dx;
            let top = this.e.offsetTop + dy;
            if (! this.lockY) this.e.style.top = top + 'px';
            if (! this.lockX) this.e.style.left = left + 'px';
        }
    }

    moveEvent(x, y) {
        // this.e.draggable = "false";
        super.moveEvent(x,y);
        let d = this.delta;
        this.moveElement(d.x, d.y);
    }
}

class ScalableDrag extends Draggable {
    constructor(selector, option = {
        mouseDown: null, 
        mouseMove: null, 
        mouseUp: null,
        lockX: false,
        lockY: false,
        relative: false,
    }, region = document.body) {

        super(selector, option, region);
        this.orgWidth = this.e.getBoundingClientRect().width;
        this.orgHeight = this.e.getBoundingClientRect().height;
        this.scale = 1;
    }

    updateOrgSize() {
        this.orgWidth = this.e.getBoundingClientRect().width;
        this.orgHeight = this.e.getBoundingClientRect().height;
    }

    setScale(scale) {
        this.scale = scale;
        this.e.style.width = this.orgWidth * scale + 'px';
        this.e.style.height = this.orgHeight * scale + 'px';
        // this.e.style.minHeight = this.orgHeight * scale + 'px';
    }

    resetScale() {
        this.scale = 1;
        this.e.style.width = '';
        this.e.style.height = '';
    }
}