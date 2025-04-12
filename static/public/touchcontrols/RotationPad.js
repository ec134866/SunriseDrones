import * as utils from './utils.js'


class RotationPad {
    container
    padElement
    region
    handle
    eventRepeatTimeout
    regionData = {}
    handleData = {}
    mouseDown = false
    mouseStopped = false

    constructor(container) {
        this.container = container
        this.padElement = document.createElement('div')
        this.padElement.classList.add('rotation-pad')
        this.region = document.createElement('div')
        this.region.classList.add('region')
        this.handle = document.createElement('div')
        this.handle.classList.add('handle')
        this.region.appendChild(this.handle)
        this.padElement.append(this.region)
        this.container.append(this.padElement)

        this.container.style.position = 'relative';

        // Aligning pad:
        let canvas = container.getElementsByTagName('canvas')[0]
        this.alignAndConfigPad(canvas)

        // events
        window.addEventListener('resize', () => {this.alignAndConfigPad(canvas)})

        // Mouse events:
        this.region.addEventListener('mousedown', (event) => {
            this.mouseDown = true
            this.handle.style.opacity = 1.0
            this.update(event.pageX, event.pageY)
        })

        document.addEventListener('mouseup', () => {
            this.mouseDown = false
            this.resetHandlePosition()
        })

        document.addEventListener('mousemove', (event) => {
            if (!this.mouseDown)
                return
            this.update(event.pageX, event.pageY)
        })

        //Touch events:
        this.region.addEventListener('touchstart', (event) => {
            event.preventDefault();
            this.mouseDown = true
            this.handle.style.opacity = 1.0
            this.update(
                event.targetTouches[0].pageX,
                event.targetTouches[0].pageY
            )
        },{ passive: false }); 

        let touchEnd = () => {
            this.mouseDown = false
            this.resetHandlePosition()
        }
        document.addEventListener('touchend', touchEnd,{ passive: false }); 
        document.addEventListener('touchcancel', touchEnd,{ passive: false }); 

        document.addEventListener('touchmove', (event) => {
            if (!this.mouseDown)
                return
            event.preventDefault();
            this.update(event.touches[0].pageX, event.touches[0].pageY)
        },{ passive: false }); 

        this.resetHandlePosition()
    }

    alignAndConfigPad(canvas){
        const containerRect = this.container.getBoundingClientRect();

        this.padElement.style.position = 'absolute';

        // this.region.offsetHeight = height of the image (100)
    
        const verticalOffset = (window.innerHeight * 0.75) - this.region.offsetHeight;
        const horizontalOffset = (containerRect.width * 0.95) - this.region.offsetWidth; 

        this.padElement.style.top = `${verticalOffset}px`;
        this.padElement.style.left = `${horizontalOffset}px`;

        // console.log("Current Container:");
        // console.log("Container ID:", this.container.id); 
        // console.log("Container Type:", this.container.tagName);


        // console.log("Container Dimensions and Position:");
        // console.log("Width:", containerRect.width);
        // console.log("Height:", containerRect.height);
        // console.log("Top:", containerRect.top);
        // console.log("Right:", containerRect.right);
        // console.log("Bottom:", containerRect.bottom);
        // console.log("Left:", containerRect.left);

        // // Log canvas dimensions
        // console.log("Canvas Dimensions:");
        // console.log("Offset Width:", canvas.offsetWidth);
        // console.log("Width:", canvas.width);
        // console.log("Offset Height:", canvas.offsetHeight);
        // console.log("Height:", canvas.height);

        // console.log("Region Dimensions:");
        // console.log("Width:", this.region.offsetWidth);
        // console.log("Height:", this.region.offsetHeight);

        // console.log("Calculating Pad Position:");
        // console.log(`Vertical Offset Calculation: (${window.innerHeight * 0.75}) - (${this.region.offsetHeight}) = ${verticalOffset}`);
        // console.log(`Horizontal Offset Calculation: (${containerRect.width} * 0.95) - (${this.region.offsetWidth}) = ${horizontalOffset}`);

        // console.log("Pad Position:");
        // console.log("Top:", this.padElement.style.top);
        // console.log("Left:", this.padElement.style.left);


        this.regionData.width = this.region.offsetWidth;
        this.regionData.height = this.region.offsetHeight;
        this.regionData.position = {
            top: this.region.offsetTop,
            left: this.region.offsetLeft
        };
        this.regionData.offset = utils.getOffset(this.region);

        // Handle height can be set directly here without radius calculations.
        this.handleData.width = this.handle.offsetWidth;
        this.handleData.height = this.handle.offsetHeight;
        
        // No need for radius calculation for the handle anymore.
        
        // Set boundaries for the handle, only vertical movement matters.
        this.regionData.top = this.regionData.position.top;
        this.regionData.bottom = this.regionData.position.top + this.regionData.height - this.handleData.height;
    }

    update(pageX, pageY) {
        let newTop = (pageY - this.regionData.offset.top)

        const minTop = 0;
        const maxTop = this.regionData.height - this.handleData.height;
        newTop = Math.max(minTop, Math.min(newTop, maxTop));

        newTop = Math.round(newTop * 10) / 10;

        // Update handle's position based on the new top.
        this.handle.style.top = `${newTop}px`;
        this.handle.style.left = `${this.regionData.centerX - this.handleData.width}px`;

        // Optionally calculate deltaY if needed for external event triggers:
        let deltaY = this.regionData.position.top + this.regionData.height / 2 - newTop;
        
        deltaY = Math.round(deltaY * 10) / 10;  // Round to one decimal place.

        this.sendEvent(0, deltaY);  // Send the event with the deltaY value.
    }

    sendEvent(dx, dy) {
        if (this.eventRepeatTimeout) {
            clearTimeout(this.eventRepeatTimeout)
        }

        if (!this.mouseDown) {
            clearTimeout(this.eventRepeatTimeout)
            return
        }

        this.eventRepeatTimeout = setTimeout(() => {
            this.sendEvent(dx, dy)
        }, 5)

        let moveEvent = new CustomEvent('move', {
            bubbles: false,
            detail: {
                'deltaX': dx,
                'deltaY': dy
            }
        })
        this.padElement.dispatchEvent(moveEvent)
    }

    resetHandlePosition() {
        
        // Shift the handle's starting position to be near the center or any position you like.
        this.handle.style.top = (this.regionData.position.top + this.regionData.height) - (this.handleData.height) + 'px';
        this.handle.style.left = this.regionData.centerX - this.handleData.width + 'px';  // Center horizontally.
        this.handle.style.opacity = 0.1; 
    }
}


export default RotationPad
