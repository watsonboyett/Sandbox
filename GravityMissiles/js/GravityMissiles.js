Physics(function(world) {

   //var ctx = document.getElementById('viewport').getContext('2d');

   var canvasWidth = window.innerWidth-8,
   canvasHeight = window.innerHeight-8,
   // bounds of the window
   viewportBounds = Physics.aabb(0, 0, canvasWidth, canvasHeight);
   
   // set up the renderer and add it to the world
   var renderer = Physics.renderer('canvas', {
      //meta: true,
      el : 'viewport', // id of the canvas element
      width : canvasWidth,
      height : canvasHeight
   });
   world.add(renderer);
   // render on each step
   world.on('step', function() {
      world.render();
   });

   Physics.behavior('body-collision-monitor', function(parent) {
      return {
         init : function(opts) {
            parent.init.call(this, opts);
         },
         connect : function(world) {
            world.on('collisions:detected', this.handleCollisions, this, 100);
         },
         disconnect : function(world) {
            world.off('collisions:detected', this.handleCollisions);
         },
         handleCollisions : function(data) {
            var cols = data.collisions, c, remBodies = [];
            for ( var i = 0, l = cols.length; i < l; i++) {
               c = cols[i];
 
               isMissileBodyA = c.bodyA.name.substring(0, 7) == "Missile";
               isMissileBodyB = c.bodyB.name.substring(0, 7) == "Missile";
               if (isMissileBodyA && isMissileBodyB) {
                  var keep, rem;
                  if (c.bodyA.mass > c.bodyB.mass) {
                     keep = c.bodyA;
                     rem = c.bodyB;
                  } else {
                     keep = c.bodyB;
                     rem = c.bodyA;
                  }
                  
                  if (c.bodyA.name == c.bodyB.name) {
                     // same team, so join the missiles
                     keep.mass = keep.mass + rem.mass;
					 rem.mass = 0;
                  } else  {
                     // different teams, so remove the missiles
                     keep.mass = keep.mass - rem.mass;     
                     rem.mass = rem.mass - keep.mass + rem.mass;
                  }

				  if (keep.mass <= 1) {
					 remBodies.push(keep);
				  } else {
				     adjustSize(keep);
				  }
                  if (rem.mass <= 1) {
				     remBodies.push(rem);
				  } else {
				     adjustSize(rem);
				  }
				  
               }
               
            }
            
            if (remBodies.length > 0) { world.remove(remBodies); }
         }
      };
   });
   var bodyJoiner = Physics.behavior('body-collision-monitor', {});

   // ensure objects bounce when ground collision is detected
   var edgeBounce = Physics.behavior('edge-collision-detection', {
      aabb : viewportBounds,
      sides : {
         left : true,
         right : true,
         top : true,
         bottom : true
      },
      restitution : 0.2,
      cof : 1
   });

   var gravity = Physics.behavior('constant-acceleration', {
      acc : {
         x : 0,
         y : 0.0002
      }
   });
   
   var bodyAttractor = Physics.behavior('newtonian', {
      strength: 0.0006
   });
   
   world.add([ 
      Physics.behavior('interactive', {el : renderer.el}),
      Physics.behavior('sweep-prune'),
      Physics.behavior('body-collision-detection'), 
      Physics.behavior('body-impulse-response'),
      bodyAttractor, 
      //gravity, 
      edgeBounce, 
      bodyJoiner // must be added after body-impulse-response, since bodyJoiner removes some bodies
   ]);

   
   var currTeam = 1;
   var clickOnPos = Physics.vector(0, 0);
   var clickOffPos = Physics.vector(0, 0);
   var currMousePos = Physics.vector(0, 0);
   var newBody;
   var isPoked = false, isHolding = false, isMoving = false, addBody = false;;
   world.on({
      'interact:grab' : function(pos) {
         clickOnPos.set(pos.x, pos.y);
         currMousePos.set(pos.x, pos.y);
      },
      'interact:poke' : function(pos) {
         clickOnPos.set(pos.x, pos.y);
         currMousePos.set(pos.x, pos.y);
         isPoked = true;
         isHolding = true;
         isMoving = false;
         
         newBody = createCircle(clickOnPos.x, clickOnPos.y, 0, 100*Math.random()+1, 0, 0, currTeam);
      },
      'interact:move' : function(data){
         if (isPoked) {
            currMousePos.set(data.x, data.y);
            
            if (currMousePos.dist(clickOnPos) < 10) {
               isHolding = true;
            } else {
               isHolding = false;
               isMoving = true;
            }
         }

         //data.body; // the body that was grabbed (if applicable)
      },
      'interact:release' : function(pos) {
         clickOffPos.set(pos.x, pos.y);
         currMousePos.set(pos.x, pos.y);
         
         if (isPoked) {
            isPoked = false;
            vx = (clickOffPos.x - clickOnPos.x) / 600;
            vy = (clickOffPos.y - clickOnPos.y) / 600;
            angle = clickOffPos.angle(clickOnPos) - Math.PI/2;
            
            //world.add(newBody); //TODO: not sure why this doesn't work properly
            world.add(createCircle(clickOnPos.x, clickOnPos.y, 0, newBody.mass, vx, vy, currTeam));
            
         }

         isHolding = false;
         isMoving = false;
         addBody = true;
      }
   });

   world.render();

   // subscribe to ticker to advance the simulation
   Physics.util.ticker.on(function(time, dt) {
      world.step(time);

      if (isHolding) {
         newBody.mass = newBody.mass * 1.10;
         adjustSize(newBody);
         renderer.drawBody(newBody, renderer.createView(newBody.geometry, newBody.sytles));
      }
      if (isMoving) {
         renderer.drawBody(newBody, renderer.createView(newBody.geometry, newBody.sytles));
         renderer.drawLine(clickOnPos, currMousePos, {
            strokeStyle : "#000000",
            lineWidth : 2,
            fillStyle : "#000000",
            lineCap : "round"
            });
      }

   });

   // resize events
   window.addEventListener('resize', function () {

      canvasWidth = window.innerWidth;
      canvasHeight = window.innerHeight;
      
      renderer.el.width = canvasWidth;
      renderer.el.height = canvasHeight;
      
      viewportBounds = Physics.aabb(0, 0, canvasWidth, canvasHeight);
      // update the boundaries
      edgeBounce.setAABB(viewportBounds);

   }, true);
   
   // start the ticker
   Physics.util.ticker.start();
   
   
   function createRandom() {
      offset = 10;
      switch (currTeam) {
         case 0:
            x = canvasWidth*Math.random();
            y = canvasHeight*Math.random();
            vx = 2*(Math.random()-0.5);
            vy = 2*(Math.random()-0.5);
            break;
         case 1:
            x = offset;
            y = canvasHeight - offset;
            vx = Math.random();
            vy = Math.random()-1;
            break;
         case 2:
            x = canvasWidth - offset;
            y = canvasHeight - offset;
            vx = Math.random()-1;
            vy = Math.random()-1;
            break;
         case 3:
            x = offset;
            y = offset;
            vx = Math.random();
            vy = Math.random();
            break;
         case 4:
            x = canvasWidth - offset;
            y = offset;
            vx = Math.random()-1;
            vy = Math.random();
            break;
      }
      v = 0.3;
      return createCircle(
         x,
         y,
         (Math.PI)*Math.random(),
         3000*Math.random()+1,
         v*vx,
         v*vy, 
         currTeam);
   }

   setInterval(function () {
      world.add(createRandom());
      currTeam = ((currTeam) % 4) + 1;
      }, 200);

});



function createCircle(x, y, angle, mass, vx, vy, team) {
   color = "#000000";
   switch (team) {
      case 0:
         color = "#000000";
         break;
      case 1:
         color = "#339966";
         break;
      case 2:
         color = "#66CCFF";
         break;
      case 3:
         color = "#996666";
         break;
      case 4:
         color = "#FF3399";
         break;
   }

   return Physics.body('circle', {
      name : "MissileC-Team" + team,
      x : x, // x-coordinate
      y : y, // y-coordinate
      vx : vx, // velocity in x-direction
      vy : vy, // velocity in y-direction
      mass : mass,
      radius : Math.log(mass),
      restitution : 0.5,
      cof : 0.9,
      styles : {
         strokeStyle : color,
         lineWidth : 1,
         fillStyle : color,
         angleIndicator : 'white'
      }
   });
}


function adjustSize(body) {
   if (body.mass <= 0) { return; }

   body.radius = Math.log(body.mass);
   body.geometry.radius = body.radius;

   body.view = undefined;
   body.recalc();
}
